# -*- coding: utf-8 -*- 

import discord
from discord.ext import commands
import youtube_dl
import csv
import pandas as pd
import os
import re
from collections import OrderedDict

bad = ['⊥', '┴', 'D쥐고', 'D지고', 'jonna', 'jot같', 'mi쳤', 'ssㅑ', 'tlqkf', 'wlfkf', '가지가지', '같은 새끼', '같은새끼', '개 새끼', '개같', '개나 소나', '개나대', '개나소나', '개넷', '개년', '개념빠가', '개독', '개돼지', '개련', '개마이', '개부랄', '개삼성', '개새기', '개새끼', '개섹', '개셈', '개소리', '개쓰래기', '개저씨', '거른다', '거지같', '그지', '계새끼', '골 빈', '골1빈', '골빈', '공개 처형', '공개처형', '관.종', '관1종', '관종', '괘새끼', '구1씹', '구씹', '그 나물에', '그1켬', '그나물에', '그따구', '그따위', '그지 같', '그지같', '그켬', '극1혐', '극혐', '글러 먹', '글러먹', '기레기', '기자레기', '김치녀', '된장녀', '피싸개', '퍄퍄', '김여사', '잼민', '아몰랑', '업계포상', '쿵쾅', '쿵.쾅', '허벌', '쿰.척', '쿰척', 'ㅗㅜㅑ', '오우야', '까내리', '껒여', '꺼지세요', '꺼져요', '로 꺼져', '로꺼져', '로 꺼.져', '꺼.지', '꼬라지', '꼴갑', '꼴값', '꼴깝', '꼴데', '꼴랑', '꼴보기', '꼴뵈기', '나빼썅', '나쁜 새끼', '넌씨눈', '년놈', '노무노무', '노알라', '노인네', '노친네', '뇌 텅', '뇌1텅', '뇌에', '뇌텅', '뇌피셜', '눈깔파', '눈새', '늬믜', '늬미', '니년', '니믜', '니미럴', '닝기리', 'ㄷㅇㅂ', '다꺼져', '닥1', '닥2', '닥전', '닥쳐라', '닥치세', '닥후', '대가리', '대갈', '더럽네', '덜떨어', '덬', '도라이', '도랏', '도랐', '도른', '돌앗구만', '돌앗나', '돌앗네', '돌았구만', '돌았나', '돌았네', '둄마', '뒈져', '뒤져라', '뒤져버', '뒤져야', '뒤져야지', '뒤져요', '뒤졌', '뒤지겠', '뒤지고싶', '뒤지길', '뒤진다', '뒤질', '듣보', '디져라', '디졌', '디지고', '디질', '딴년', '또라이', '또라인', '똘아이', '뚝배기', '뚫린 입', '뚫린입', '라면갤', '런년', '럼들', '레1친', '레기같', '레기네', '레기다', '레친', '롬들', 'ㅁ.ㄱ', 'ㅁㅊ', 'ㅁ친', '미새', '막 내뱉', '막내뱉', '맘충', '망돌', '망해라', '머갈', '머리 텅', '머리텅', '먹.금', '먹.끔', '먹1금', '먹금', '먹끔', '명존', '무개념', '뭐래는', '뭐임', '뭐저래', '뭔솔', '믜칀', '믜친', '미: 놈', '미:놈', '미1친', '미놈', '미시친발', '미쳣네', '미쳤나', '미쳤니', '미췬', '미칀', '미친 새', '미친~', '미친개', '미친새', '미친색', '미친ㅋ', '미틴', '및힌', 'ㅂㄹ', 'ㅂㅁㄱ', 'ㅂㅊ', 'ㅂ크', '발놈', '별창', '병1신', '병1크', '병맛', '병신', '병크', '봊', '븅신', '빠큐', '빡새끼', '빻았', '빻은', '뻐규', '뻐큐', '뻑유', '뻑큐', '뻨큐', '뼈큐', '뽄새', '뽄세', '삐걱', 'ㅄ', 'ㅅ,ㅂ', 'ㅅ.ㅂ', 'ㅅ1ㅂ', 'ㅅ1발', 'ㅅㄲ네', 'ㅅㄲ들', 'ㅅ루', 'ㅅㅋ', 'ㅅㅌㅊ', 'ㅅㅡ루', '사새끼', '새.끼', '새1끼', '새1키', '새77ㅣ', '새끼라', '새끼야', '새퀴', '새킈', '새키', '색희', '색히', '샊기', '샊히', '샹년', '섀키', '서치해', '섬숭이', '성괴', '솔1친', '솔친', '수준하고는', '쉬발', '쉬버', '쉬이바', '쉬이이', '쉬이이이', '쉬펄', '슈1발', '슈레기', '슈발', '슈벌', '슈우벌', '슈ㅣ발', '스.루', '스ㄹㅜ', '스벌', '스죄', '스타죄국', '슨상님', '싑창', '시1발', '시미발친', '시미친발', '시바 ', '시바라지', '시바류', '시바시바', '시바알', '시바앙', '시발', '시방새', '시벌탱', '시볼탱', '시부럴', '시부렬', '시부울', '시뷰럴', '시뷰렬', '시빨', '시새발끼', '시이발', '시친발미', '시키가', '시팔', '시펄', '십창', '십팔', 'ㅆ1ㄺ', 'ㅆ1ㅂ', 'ㅆㄹㄱ', 'ㅆㄺ', 'ㅆㅂ', '싸가지 없', '싸가지없', '싸물어', '쌉가', '쌍년', '쌍놈', '쌔끼', '썅', '썌끼', '쒸펄', '쓰1레기', '쓰래기같', '쓰레기 새', '쓰레기새', '쓰렉', '씝창', '씨1발', '씨바라', '씨바알', '씨발', '씨방새', '씨버럼', '씨벌', '씨벌탱', '씨볼탱', '씨부럴', '씨부렬', '씨뷰럴', '씨뷰렬', '씨빠빠', '씨빨', '씨뻘', '씨새발끼', '씨이발', '씨팔', '씹귀', '씹덕', '씹못', '씹뻐럴', '씹새끼', '씹쌔', '씹창', '씹치', '씹팔', '씹할', 'ㅇㅍㅊㅌ', 'ㅇㅒ쁜', '아가리', '아닥', '오타쿠', '오탁후', '오덕후', '오덕', '더쿠', '아오 ㅅㅂ', '아오 시바', '아오ㅅㅂ', '아오시바', '안물안궁', '애미', '앰', '앰창', '얘쁘', '얘쁜', '얪', '에라이 퉤', '에라이 퉷', '에라이퉤', '에라이퉷', '엠뷩신', '엠븽신', '엠빙신', '엠생', '엠창', '엿같', '엿이나', '예.질', '예1질', '예질', '옘병', '오크', '와꾸', '왜저럼', '외1퀴', '외퀴', '웅앵', '웅엥', '은년', '은새끼', '이 새끼', '이따위', '이새끼', '인간말종', '입털', 'ㅈ.ㄴ', 'ㅈ소', 'ㅈㄴ', 'ㅈㄹ', '자업자득', '작작', '잘또', '저따위', '지잡', '검머외', '절라', '정병', '정신나갓', '정신나갔', '젖 같', '젗같', '젼나', '젼낰', '졀라', '졀리', '졌같은', '졏 같', '조낸', '조녜', '조온', '조온나', '족까', '존 나', '존,나', '존.나', '존1', '존1나', '존귀', '존귘', '존ㄴ나', '존나', '존낙', '존내', '존똑', '존맛', '존멋', '존버', '존싫', '존쎄', '존쎼', '존예', '존웃', '존잘', '존잼', '존좋', '존트', '졸귀', '졸귘', '졸라 ', '졸맛', '졸멋', '졸싫', '졸예', '졸웃', '졸잼', '졸좋', '좁밥', '조센징', '짱깨', '짱개', '짱꼴라', '꼴라', '착짱', '죽짱', '짱골라', '좃', '종나', '좆', '좆까', '좇같', '죠낸', '죠온나', '죤나', '죤내', '죵나', '죶', '죽어버려', '죽여 버리고', '죽여버리고', '죽여불고', '죽여뿌고', '중립충', '줬같은', '쥐랄', '쥰나', '쥰내', '쥰니', '쥰트', '즤랄', '지 랄', '지1랄', '지1뢰', '지껄이', '지들이', '지랄', '지롤', '지뢰', '지인지조', 'ㅉ', 'ㅉ질한', '짱께', '쪼녜', '쪼다', '착짱죽짱', '쪽본', '쪽1바리', '쪽바리', '쪽발', '쫀 맛', '쫀1', '쫀귀', '쫀맛', '쫂', '쫓같', '쬰잘', '쬲', '쯰질', '찌1질', '찌질한', '찍찍이', '찎찎이', '찝째끼', '창년', '창녀', '창놈', '창넘', '처먹', '凸', '첫빠', '쳐마', '쳐먹', '쳐받는', '쳐발라', '취ㅈ', '취좃', '친 년', '친 놈', '친구년', '친년', '친노마', '친놈', '텐귀', '텐덕', '톡디', 'ㅍㅌㅊ', '파1친', '파친', '핑1프', '핑거프린세스', '핑끄', '핑프', 'ㅎㅃ', 'ㅎㅌㅊ', '헛소리', '손놈', '남미새', '여미새', '혐석', '호로새끼', '호로잡', '화낭년', '화냥년', '후.려', '후1려', '후1빨', '후려', '후빨', 'ㅗ', '섹스', '  ', '4r5e', '5h1t', '5hit', 'a55', 'anal', 'anus', 'ar5e', 'arrse', 'arse', 'ass', 'ass-fucker', 'asses', 'assfucker', 'assfukka', 'asshole', 'assholes', 'asswhole', 'a_s_s', 'b!tch', 'b00bs', 'b17ch', 'b1tch', 'ballbag', 'balls', 'ballsack', 'bastard', 'beastial', 'beastiality', 'bellend', 'bestial', 'bestiality', 'bi+ch', 'biatch', 'bitch', 'bitcher', 'bitchers', 'bitches', 'bitchin', 'bitching', 'bloody', 'blow job', 'blowjob', 'blowjobs', 'boiolas', 'bollock', 'bollok', 'boner', 'boob', 'boobs', 'booobs', 'boooobs', 'booooobs', 'booooooobs', 'breasts', 'buceta', 'bugger', 'bum', 'bunny fucker', 'butt', 'butthole', 'buttmunch', 'buttplug', 'c0ck', 'c0cksucker', 'carpet muncher', 'cawk', 'chink', 'cipa', 'cl1t', 'clit', 'clitoris', 'clits', 'cnut', 'cock', 'cock-sucker', 'cockface', 'cockhead', 'cockmunch', 'cockmuncher', 'cocks', 'cocksuck ', 'cocksucked ', 'cocksucker', 'cocksucking', 'cocksucks ', 'cocksuka', 'cocksukka', 'cok', 'cokmuncher', 'coksucka', 'coon', 'cox', 'crap', 'cum', 'cummer', 'cumming', 'cums', 'cumshot', 'cunilingus', 'cunillingus', 'cunnilingus', 'cunt', 'cuntlick ', 'cuntlicker ', 'cuntlicking ', 'cunts', 'cyalis', 'cyberfuc', 'cyberfuck ', 'cyberfucked ', 'cyberfucker', 'cyberfuckers', 'cyberfucking ', 'd1ck', 'damn', 'dick', 'dickhead', 'dildo', 'dildos', 'dink', 'dinks', 'dirsa', 'dlck', 'dog-fucker', 'doggin', 'dogging', 'donkeyribber', 'doosh', 'duche', 'dyke', 'ejaculate', 'ejaculated', 'ejaculates ', 'ejaculating ', 'ejaculatings', 'ejaculation', 'ejakulate', 'f u c k', 'f u c k e r', 'f4nny', 'fag', 'fagging', 'faggitt', 'faggot', 'faggs', 'fagot', 'fagots', 'fags', 'fanny', 'fannyflaps', 'fannyfucker', 'fanyy', 'fatass', 'fcuk', 'fcuker', 'fcuking', 'feck', 'fecker', 'felching', 'fellate', 'fellatio', 'fingerfuck ', 'fingerfucked ', 'fingerfucker ', 'fingerfuckers', 'fingerfucking ', 'fingerfucks ', 'fistfuck', 'fistfucked ', 'fistfucker ', 'fistfuckers ', 'fistfucking ', 'fistfuckings ', 'fistfucks ', 'flange', 'fook', 'fooker', 'fuck', 'fucka', 'fucked', 'fucker', 'fuckers', 'fuckhead', 'fuckheads', 'fuckin', 'fucking', 'fuckings', 'fuckingshitmotherfucker', 'fuckme ', 'fucks', 'fuckwhit', 'fuckwit', 'fudge packer', 'fudgepacker', 'fuk', 'fuker', 'fukker', 'fukkin', 'fuks', 'fukwhit', 'fukwit', 'fux', 'fux0r', 'f_u_c_k', 'gangbang', 'gangbanged ', 'gangbangs ', 'gaylord', 'gaysex', 'goatse', 'God', 'god-dam', 'god-damned', 'goddamn', 'goddamned', 'hardcoresex ', 'hell', 'heshe', 'hoar', 'hoare', 'hoer', 'homo', 'hore', 'horniest', 'horny', 'hotsex', 'jack-off ', 'jackoff', 'jap', 'jerk-off ', 'jism', 'jiz ', 'jizm ', 'jizz', 'kawk', 'knob', 'knobead', 'knobed', 'knobend', 'knobhead', 'knobjocky', 'knobjokey', 'kock', 'kondum', 'kondums', 'kum', 'kummer', 'kumming', 'kums', 'kunilingus', 'l3i+ch', 'l3itch', 'labia', 'lmfao', 'lust', 'lusting', 'm0f0', 'm0fo', 'm45terbate', 'ma5terb8', 'ma5terbate', 'masochist', 'master-bate', 'masterb8', 'masterbat*', 'masterbat3', 'masterbate', 'masterbation', 'masterbations', 'masturbate', 'mo-fo', 'mof0', 'mofo', 'mothafuck', 'mothafucka', 'mothafuckas', 'mothafuckaz', 'mothafucked ', 'mothafucker', 'mothafuckers', 'mothafuckin', 'mothafucking ', 'mothafuckings', 'mothafucks', 'mother fucker', 'motherfuck', 'motherfucked', 'motherfucker', 'motherfuckers', 'motherfuckin', 'motherfucking', 'motherfuckings', 'motherfuckka', 'motherfucks', 'muff', 'mutha', 'muthafecker', 'muthafuckker', 'muther', 'mutherfucker', 'n1gga', 'n1gger', 'nazi', 'nigg3r', 'nigg4h', 'nigga', 'niggah', 'niggas', 'niggaz', 'nigger', 'niggers ', 'nob', 'nob jokey', 'nobhead', 'nobjocky', 'nobjokey', 'numbnuts', 'nutsack', 'orgasim ', 'orgasims ', 'orgasm', 'orgasms ', 'p0rn', 'pawn', 'pecker', 'penis', 'penisfucker', 'phonesex', 'phuck', 'phuk', 'phuked', 'phuking', 'phukked', 'phukking', 'phuks', 'phuq', 'pigfucker', 'pimpis', 'piss', 'pissed', 'pisser', 'pissers', 'pisses ', 'pissflaps', 'pissin ', 'pissing', 'pissoff ', 'poop', 'porn', 'porno', 'pornography', 'pornos', 'prick', 'pricks ', 'pron', 'pube', 'pusse', 'pussi', 'pussies', 'pussy', 'pussys ', 'rectum', 'retard', 'rimjaw', 'rimming', 's hit', 's.o.b.', 'sadist', 'schlong', 'screwing', 'scroat', 'scrote', 'scrotum', 'semen', 'sex', 'sh!+', 'sh!t', 'sh1t', 'shag', 'shagger', 'shaggin', 'shagging', 'shemale', 'shi+', 'shit', 'shitdick', 'shite', 'shited', 'shitey', 'shitfuck', 'shitfull', 'shithead', 'shiting', 'shitings', 'shits', 'shitted', 'shitter', 'shitters ', 'shitting', 'shittings', 'shitty ', 'skank', 'slut', 'sluts', 'smegma', 'smut', 'snatch', 'son-of-a-bitch', 'spac', 'spunk', 's_h_i_t', 't1tt1e5', 't1tties', 'teets', 'teez', 'testical', 'testicle', 'tit', 'titfuck', 'tits', 'titt', 'tittie5', 'tittiefucker', 'titties', 'tittyfuck', 'tittywank', 'titwank', 'tosser', 'turd', 'tw4t', 'twat', 'twathead', 'twatty', 'twunt', 'twunter', 'v14gra', 'v1gra', 'vagina', 'viagra', 'vulva', 'w00se', 'wang', 'wank', 'wanker', 'wanky', 'whoar', 'whore', 'willies', 'willy', 'xrated', 'xxx', '3p', 'g スポット', 's ＆ m', 'sm', 'sm女王', 'xx', 'アスホール', 'アナリングス', 'アナル', 'いたずら', 'イラマチオ', 'エクスタシー', 'エスコート', 'エッチ', 'エロティズム', 'エロティック', 'オーガズム', 'オカマ', 'おしっこ', 'おしり', 'オシリ', 'おしりのあな', 'おっぱい', 'オッパイ', 'オナニー', 'オマンコ', 'おもらし', 'お尻', 'カーマスートラ', 'カント', 'クリトリス', 'グループ・セックス', 'グロ', 'クンニリングス', 'ゲイ・セックス', 'ゲイボーイ', 'ゴールデンシャワー', 'コカイン', 'ゴックン', 'サディズム', 'しばり', 'スウィンガー', 'スカートの中', 'スカトロ', 'ストラップオン', 'ストリップ劇場', 'スラット', 'スリット', 'セクシーな', 'セクシーな 10 代', 'セックス', 'ソドミー', 'ちんこ', 'ディープ・スロート', 'ディック', 'ディルド', 'デートレイプ', 'デブ', 'テレフォンセックス', 'ドッグスタイル', 'トップレス', 'なめ', 'ニガー', 'ヌード', 'ネオ・ナチ', 'ハードコア', 'パイパン', 'バイブレーター', 'バック・スタイル', 'パンティー', 'ビッチ', 'ファック', 'ファンタジー', 'フィスト', 'フェティッシュ', 'フェラチオ', 'ふたなり', 'ぶっかけ', 'フック', 'プリンス アルバート ピアス', 'プレイボーイ', 'ベアバック', 'ペニス', 'ペニスバンド', 'ボーイズラブ', 'ボールギャグ', 'ぽっちゃり', 'ホモ', 'ポルノ', 'ポルノグラフィー', 'ボンテージ', 'マザー・ファッカー', 'マスターベーション', 'まんこ', 'やおい', 'やりまん', 'ラティーナ', 'ラバー', 'ランジェリー', 'レイプ', 'レズビアン', 'ローター', 'ロリータ', '淫乱', '陰毛', '革抑制', '騎上位', '巨根', '巨乳', '強姦犯', '玉なめ', '玉舐め', '緊縛', '近親相姦', '嫌い', '後背位', '合意の性交', '拷問', '殺し方', '殺人事件', '殺人方法', '支配', '児童性虐待', '自己愛性', '射精', '手コキ', '獣姦', '女の子', '女王様', '女子高生', '女装', '新しいポルノ', '人妻', '人種', '性交', '正常位', '生殖器', '精液', '挿入', '足フェチ', '足を広げる', '大陰唇', '脱衣', '茶色のシャワー', '中出し', '潮吹き女', '潮吹き男性', '直腸', '剃毛', '貞操帯', '奴隷', '二穴', '乳首', '尿道プレイ', '覗き', '売春婦', '縛り', '噴出', '糞', '糞尿愛好症', '糞便', '平手打ち', '変態', '勃起する', '夢精', '毛深い', '誘惑', '幼児性愛者', '裸', '裸の女性', '乱交', '両性', '両性具有', '両刀', '輪姦', '卍', '宦官', '肛門', '膣', '강간', '개자식', '개좆', '개차반', '거유', '계집년', '고자', '근친', '노모', '니기미', '뒤질래', '딸딸이', '때씹', '뙤놈', '로리타', '망가', '몰카', '미친', '미친새끼', '바바리맨', '변태', '보지', '불알', '빠구리', '사까시', '스와핑', '씨발놈', '씹', '씹물', '씹빨', '씹알', '암캐', '애자', '야동', '야사', '야애니', '엄창', '에로', '염병', '유모', '육갑', '은꼴', '자위', '자지', '잡년', '종간나', '좆만', '죽일년', '쥐좆', '직촬', '포르노', '하드코어', '호로', '후레아들', '후장', '희쭈그리', '2g1c', '2 girls 1 cup', 'acrotomophilia', 'alabama hot pocket', 'alaskan pipeline', 'anilingus', 'apeshit', 'arsehole', 'assmunch', 'auto erotic', 'autoerotic', 'babeland', 'baby batter', 'baby juice', 'ball gag', 'ball gravy', 'ball kicking', 'ball licking', 'ball sack', 'ball sucking', 'bangbros', 'bangbus', 'bareback', 'barely legal', 'barenaked', 'bastardo', 'bastinado', 'bbw', 'bdsm', 'beaner', 'beaners', 'beaver cleaver', 'beaver lips', 'big black', 'big breasts', 'big knockers', 'big tits', 'bimbos', 'birdlock', 'black cock', 'blonde action', 'blonde on blonde action', 'blow your load', 'blue waffle', 'blumpkin', 'bollocks', 'bondage', 'booty call', 'brown showers', 'brunette action', 'bukkake', 'bulldyke', 'bullet vibe', 'bullshit', 'bung hole', 'bunghole', 'busty', 'buttcheeks', 'camel toe', 'camgirl', 'camslut', 'camwhore', 'carpetmuncher', 'chocolate rosebuds', 'cialis', 'circlejerk', 'cleveland steamer', 'clover clamps', 'clusterfuck', 'coprolagnia', 'coprophilia', 'cornhole', 'coons', 'creampie', 'cumshots', 'darkie', 'date rape', 'daterape', 'deep throat', 'deepthroat', 'dendrophilia', 'dingleberry', 'dingleberries', 'dirty pillows', 'dirty sanchez', 'doggie style', 'doggiestyle', 'doggy style', 'doggystyle', 'dog style', 'dolcett', 'domination', 'dominatrix', 'dommes', 'donkey punch', 'double dong', 'double penetration', 'dp action', 'dry hump', 'dvda', 'eat my ass', 'ecchi', 'erotic', 'erotism', 'escort', 'eunuch', 'fecal', 'felch', 'feltch', 'female squirting', 'femdom', 'figging', 'fingerbang', 'fingering', 'fisting', 'foot fetish', 'footjob', 'frotting', 'fuck buttons', 'fucktards', 'futanari', 'gang bang', 'gay sex', 'genitals', 'giant cock', 'girl on', 'girl on top', 'girls gone wild', 'goatcx', 'god damn', 'gokkun', 'golden shower', 'goodpoop', 'goo girl', 'goregasm', 'grope', 'group sex', 'g-spot', 'guro', 'hand job', 'handjob', 'hard core', 'hardcore', 'hentai', 'homoerotic', 'honkey', 'hooker', 'hot carl', 'hot chick', 'how to kill', 'how to murder', 'huge fat', 'humping', 'incest', 'intercourse', 'jack off', 'jail bait', 'jailbait', 'jelly donut', 'jerk off', 'jigaboo', 'jiggaboo', 'jiggerboo', 'juggs', 'kike', 'kinbaku', 'kinkster', 'kinky', 'knobbing', 'leather restraint', 'leather straight jacket', 'lemon party', 'livesex', 'lolita', 'lovemaking', 'make me come', 'male squirting', 'masturbating', 'masturbation', 'menage a trois', 'milf', 'missionary position', 'mong', 'mound of venus', 'mr hands', 'muff diver', 'muffdiving', 'nambla', 'nawashi', 'negro', 'neonazi', 'nig nog', 'nimphomania', 'nipple', 'nipples', 'nsfw', 'nsfw images', 'nude', 'nudity', 'nutten', 'nympho', 'nymphomania', 'octopussy', 'omorashi', 'one cup two girls', 'one guy one jar', 'orgy', 'paedophile', 'paki', 'panties', 'panty', 'pedobear', 'pedophile', 'pegging', 'phone sex', 'piece of shit', 'pikey', 'piss pig', 'pisspig', 'playboy', 'pleasure chest', 'pole smoker', 'ponyplay', 'poof', 'poon', 'poontang', 'punany', 'poop chute', 'poopchute', 'prince albert piercing', 'pthc', 'pubes', 'queaf', 'queef', 'quim', 'raghead', 'raging boner', 'rape', 'raping', 'rapist', 'reverse cowgirl', 'rimjob', 'rosy palm', 'rosy palm and her 5 sisters', 'rusty trombone', 'sadism', 'santorum', 'scat', 'scissoring', 'sexcam', 'sexo', 'sexy', 'sexual', 'sexually', 'sexuality', 'shaved beaver', 'shaved pussy', 'shibari', 'shitblimp', 'shitty', 'shota', 'shrimping', 'skeet', 'slanteye', 's&m', 'snowballing', 'sodomize', 'sodomy', 'spastic', 'spic', 'splooge', 'splooge moose', 'spooge', 'spread legs', 'strap on', 'strapon', 'strappado', 'strip club', 'style doggy', 'suck', 'sucks', 'suicide girls', 'sultry women', 'swastika', 'swinger', 'tainted love', 'taste my', 'tea bagging', 'threesome', 'throating', 'thumbzilla', 'tied up', 'tight white', 'titty', 'tongue in a', 'topless', 'towelhead', 'tranny', 'tribadism', 'tub girl', 'tubgirl', 'tushy', 'twink', 'twinkie', 'two girls one cup', 'undressing', 'upskirt', 'urethra play', 'urophilia', 'venus mound', 'vibrator', 'violet wand', 'vorarephilia', 'voyeur', 'voyeurweb', 'voyuer', 'wetback', 'wet dream', 'white power', 'worldsex', 'wrapping men', 'wrinkled starfish', 'yaoi', 'yellow showers', 'yiffy', 'zoophilia', '🖕']

bot = commands.Bot(command_prefix='>')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=">도움"))
f = open('database.csv', 'w', encoding='utf-8', newline='\n')
wr = csv.writer(f)
m=0
while m<1:
    m=1
    wr.writerow(['mal', 'mal1'])
    f.close()
    
@bot.event 
async def on_message(message):
    message_contant=message.content
    for i in bad:
        if i in message_contant:
            await message.channel.send('욕설이 감지되어 메세지를 삭제했습니다.')
            await message.delete()

            
@bot.command()
async def 초기화(ctx, id, pw):
    if id == 'jm0730':
        if pw == 'jmjmjm0730':
            await ctx.send('데이터베이스를 초기화합니다.')
            f = open('database.csv', 'w', encoding='utf-8', newline='\n')
            wr = csv.writer(f)
            wr.writerow(['mal', 'mal1'])
            f.close()
        else:
            await ctx.send('비밀번호가 잘못되었습니다.')
    else:
        await ctx.send('ID가 잘못되었습니다.')

@bot.command()
async def 도움(ctx):
    embed=discord.Embed(title="명령어 목록", description="아주좋은봇", color=0x4400ff)
    embed.add_field(name=">배워 [대상] [설명]", value="[대상]이 [설명]임을 배웁니다.", inline=False)
    embed.add_field(name=">말해 [대상]", value="[대상]에 대해 말합니다.", inline=False)
    embed.add_field(name=">핑", value="봇의 핑을 확인합니다.", inline=False)
    embed.add_field(name=">재생 [Youtube URL]", value="음성 채널에서 노래를 재생합니다.", inline=False)
    embed.add_field(name=">일시정지", value="노래를 일시정지 합니다.", inline=False)
    embed.add_field(name=">다시시작", value="일시정지된 노래를 다시 재생합니다.", inline=False)
    embed.add_field(name=">멈춰", value="노래를 멈춥니다.", inline=False)
    embed.add_field(name=">나가", value="봇이 음성 채널에서 나갑니다.", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def 배워(ctx, mal, mal1):
    text_mod = re.sub('[^정지민]','',mal)
    text_mod1 = re.sub('[^정지민]','',mal1)
    a_str = text_mod
    a_str1 = text_mod1
    if '정지민' in ''.join(OrderedDict.fromkeys(a_str)):
        await ctx.send('정지민이 들어간 말은 배울 수 없어요!')
        await ctx.send('https://media.tenor.com/images/bc112882a77db08c53e072765be4fe1e/tenor.gif')
    elif '정지민' in ''.join(OrderedDict.fromkeys(a_str1)):
        await ctx.send('정지민이 들어간 말은 배울 수 없어요!')
        await ctx.send('https://media.tenor.com/images/bc112882a77db08c53e072765be4fe1e/tenor.gif')
    else:
        f = open('database.csv', 'a', encoding='utf-8', newline='\n')
        wr = csv.writer(f)
        wr.writerow([mal, mal1])
        f.close()
        await ctx.send(mal + ' 이/가 ' + mal1 + '이라구요? 기억했어요.')

@bot.command()
async def 말해(ctx, mall1):
    abc = pd.read_csv('database.csv')
    df = pd.DataFrame(abc)
    aabb = df[df['mal'] == mall1]
    aabbb = str(aabb).split(' ')
    await ctx.send(aabbb[-1])

@bot.command()
async def 핑(ctx):
    await ctx.send('퐁! {0}'.format(round(bot.latency, 1)))

@bot.command()
async def 재생(ctx, url):
    channel = ctx.author.voice.channel
    if bot.voice_clients == []:
    	await channel.connect()
    	await ctx.send(str(bot.voice_clients[0].channel) + "에 연결되었어요.")

    ydl_opts = {'format': 'bestaudio'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
    voice = bot.voice_clients[0]
    await ctx.send("현재 재생중 : " + url)
    voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))

@bot.command()
async def 일시정지(ctx):
    if not bot.voice_clients[0].is_paused():
        bot.voice_clients[0].pause()
    else:
        await ctx.send("이미 멈춰 있어요.")

@bot.command()
async def 다시시작(ctx):
    if bot.voice_clients[0].is_paused():
        bot.voice_clients[0].resume()
    else:
        await ctx.send("이미 재생중이에요.")
        
@bot.command()
async def 멈춰(ctx):
    if bot.voice_clients[0].is_playing():
    	bot.voice_clients[0].stop()
    else:
    	await ctx.send("재생중이 아니에요.")

@bot.command()
async def 나가(ctx):
    if bot.voice_clients[0].is_playing():
        await bot.voice_clients[0].disconnect()
        

bot.run('Token')
