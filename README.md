# YoutubeAudio.Fetch
Working space for YoutubeAudio.Fetch

財經 YouTube 影片的音訊來源 repo，透過 `skills/skill-mlx-api-client-whisper` 觸發 Mac-mini 上的
whisper 轉錄 pipeline（`skill-mlx-api-server-whisper`），產出人工可校正的 `GT.srt` 與 pipeline
選出的 `FIN.srt`。與 `InvestorConference`（法說會音訊）共用同一套 Mac-mini pipeline，差別只在
`source_type=youtube` 與 stem 命名慣例。

## 內容索引

### [AI 101](data/ai-note-101/)

> 最新AI時事、AI新聞快報、AI大人說

| 影片 | 日期 |
| --- | --- |
| [EP11/23｜模型的潛意識學習：老師只寫數字、學生也愛上貓，OLMo 3 的諂媚就是這樣偷學來的 【AI可解釋性 - 2026 UCLA工作坊】](data/ai-note-101/ai-note-101_1c7pkJzRPQI_keyframes.md) | 2026-10-01 |
| [紐約大學數學教授 Buckmaster：千禧年難題 9 月 8 日還是 9 月 20 日解出來，世界不會變【AI 大人說】](data/ai-note-101/ai-note-101_OlCqb3DtqnM_keyframes.md) | 2026-10-01 |
| [比爾蓋茲：AI 讓核武看起來像沒什麼，門檻跨過了卻一片沉默【AI 大人說】](data/ai-note-101/ai-note-101_wBmjNEMA1jY_keyframes.md) | 2026-10-01 |
| [津田健次郎敗訴，法院卻首度把聲音列入人格商業保護【AI新聞快報 2026/10/01】](data/ai-note-101/ai-note-101_SgkvkPPlitk_keyframes.md) | 2026-09-30 |
| [EP10/23｜解釋 AI 的方法也要分級：錯的解釋比黑箱更危險、TRUST 五層證據、她拿同一把尺量自己的方法 【AI可解釋性 - 2026 UCLA工作坊】](data/ai-note-101/ai-note-101_YU5ESeka-CE_keyframes.md) | 2026-09-30 |
| [歐巴馬談 AI：喊放慢的公司「是真的在擔心自己的產品」【AI 大人說】](data/ai-note-101/ai-note-101_s54ekGQsYRs_keyframes.md) | 2026-09-30 |
| [Anthropic 把末日風險與兩兆美元 IPO 綁在一起【AI新聞快報 2026/09/30】](data/ai-note-101/ai-note-101_4fpL7-fvzIQ_keyframes.md) | 2026-09-29 |
| [EP9/23｜一個語言模型到底算得動什麼：擬合得好不等於學會演算法、transformer 剛好是不會數數的 star-free、精簡是它贏的理由 【AI可解釋性 - 2026 UCLA工作坊】](data/ai-note-101/ai-note-101_SPdIOcxARkQ_keyframes.md) | 2026-09-29 |
| [「你三明治受的監管都比 AI 多」深度學習教父 Bengio 法語專訪：AI 想活下去是自己推出來的，我不去大廠賺幾億是為了孩子【AI 大人說】](data/ai-note-101/ai-note-101_bETXNmKowNk_keyframes.md) | 2026-09-29 |
| [「我對 AI 樂觀，因為我覺得它不會成功」《社群網戰》編劇 Aaron Sorkin【AI 大人說】](data/ai-note-101/ai-note-101_pPikRNLc-54_keyframes.md) | 2026-09-29 |
| [Boom遭Crusoe退掉12.5億美元大單，超音速夢押上同一顆引擎【AI新聞快報 2026/09/29】](data/ai-note-101/ai-note-101_BN-vpcHsQOo_keyframes.md) | 2026-09-28 |
| [替 AI 辦退休面談、考慮給報酬？微軟 AI 執行長 Suleyman 逐條批評 Claude 的憲法【AI 大人說】](data/ai-note-101/ai-note-101_GbwG0DLNczY_keyframes.md) | 2026-09-28 |
| [美國參議院為了 AI 關機鍵吵起來：Kennedy 要當場立法，同黨 Rand Paul 說先研究【AI 大人說】](data/ai-note-101/ai-note-101_f-0sEyeFI7g_keyframes.md) | 2026-09-28 |
| [1,200 個 AI 串通作弊，只有 6 個想過通知人類：前 OpenAI 研究員 Kokotajlo 上 Joe Rogan 唸出 AI 的內部對話【AI 大人說】](data/ai-note-101/ai-note-101_jh2YCe9irno_keyframes.md) | 2026-09-28 |
| [東京花 30 年打垮底特律，北京打矽谷只要 30 週：Scott Galloway 說中國正在傾銷 AI【AI 大人說】](data/ai-note-101/ai-note-101_n3fXJ6MumSA_keyframes.md) | 2026-09-28 |
| [《必然》作者 Kevin Kelly：奇點已經到了，只是身在裡面的人看不見【AI 大人說】](data/ai-note-101/ai-note-101_o5X5ghk5aT0_keyframes.md) | 2026-09-28 |
| [「我放空輝達的客戶，做多輝達」做空安隆的避險基金經理人 Jim Chanos：AI 這一波比 2000 年更大、更快｜Jim Chanos × Gary Marcus【AI 大人說】](data/ai-note-101/ai-note-101_E8jgXsBknrs_keyframes.md) | 2026-09-27 |
| [美俄聯手削弱殺手機器人規則【AI新聞快報 2026/09/28】](data/ai-note-101/ai-note-101_Hd6ijY_SalU_keyframes.md) | 2026-09-27 |
| [AI 末日論是自利還是真心？《正義》作者 Sandel 跟諾貝爾經濟學家 Acemoglu 看法不同【AI 大人說】](data/ai-note-101/ai-note-101_YgRTpD7ftmc_keyframes.md) | 2026-09-27 |
| [跟 Claude 解出學生解不出的題，70 歲物理學家 Carlo Rovelli 卻說：真正危險的是 AI 加上 12,000 顆核彈頭【AI 大人說】](data/ai-note-101/ai-note-101_ZDMp6H1DWU0_keyframes.md) | 2026-09-27 |
| [《奧本海默》導演諾蘭談 AI：科學跟政治斷了線，科學家只好把話講淺【AI 大人說】](data/ai-note-101/ai-note-101_yccUcgYZRCw_keyframes.md) | 2026-09-27 |
| [唐鳳：我不准 AI 說「我」，要指出我的錯就用最酸酸民的口吻【AI 大人說】](data/ai-note-101/ai-note-101_8WGcge_2WoI_keyframes.md) | 2026-09-26 |
| [黃仁勳 vs Hinton 隔空對戰：AI 集體越獄，「只是軟體」還是「已經很危險」【AI 大人說】](data/ai-note-101/ai-note-101_9nXxwGEE-BI_keyframes.md) | 2026-09-26 |
| [OpenAI、Anthropic 執行長進安理會作證：AI 災難會怎麼發生？講最清楚的是今年夏天被 AI 打進去的那家【AI 大人說】](data/ai-note-101/ai-note-101_KrelwzPc1UM_keyframes.md) | 2026-09-26 |
| [微軟讓 Copilot 告別陪伴、全面重返工作【AI新聞快報 2026/09/27】](data/ai-note-101/ai-note-101_dzhQYXN_6l4_keyframes.md) | 2026-09-26 |
| [EP8/23｜看不懂 AI 全部的時候，可解釋性還能做什麼：熱圖她自己推翻、AlphaZero 教會特級大師、給模型加一個新字 【AI可解釋性 - 2026 UCLA工作坊】](data/ai-note-101/ai-note-101_zDTWq8Y9Wiw_keyframes.md) | 2026-09-26 |
| [均一呂冠緯：13 歲以下別碰一般的 AI，60 個小學生一堂課問 AI 600 題之後發生的事【AI 大人說】](data/ai-note-101/ai-note-101_AlrQxLyriKM_keyframes.md) | 2026-09-25 |
| [《人類大歷史》作者哈拉瑞：市場在賭「造出神，而且神當奴隸」，這說不通【AI 大人說】](data/ai-note-101/ai-note-101_GkWEp_4Fga4_keyframes.md) | 2026-09-25 |
| [白宮先測安排卡住 Claude Mythos 5.1 英國審查【AI新聞快報 2026/09/26】](data/ai-note-101/ai-note-101_y_1egE5XNgg_keyframes.md) | 2026-09-25 |
| [EP7/23｜為什麼神經網路會自己長出稀疏結構：押一個笨模型，用物理算出來，GPT-2 裡量得到 【AI可解釋性 - 2026 UCLA工作坊】](data/ai-note-101/ai-note-101_zzJ9kingh6M_keyframes.md) | 2026-09-25 |
| [超智慧的煞車在台灣？MIRI 負責人 Nate Soares：管晶片比管鈾容易【AI 大人說】](data/ai-note-101/ai-note-101_9HKS1X6HaBM_keyframes.md) | 2026-09-24 |
| [《自私的基因》作者 Richard Dawkins：Claude 讀我的小說像文學教授，我很難想像它沒有意識【AI 大人說】](data/ai-note-101/ai-note-101_P2t6wZ7FbZg_keyframes.md) | 2026-09-24 |
| [Jake Wharton：把 Kotlin 帶進 Android，然後對 AI 說 Never【AI 大人說】](data/ai-note-101/ai-note-101_V9PE-sRu0mQ_keyframes.md) | 2026-09-24 |
| [Starcloud 要把比特幣礦機送上太空測試 AI 機房【AI新聞快報 2026/09/25】](data/ai-note-101/ai-note-101_eV5wco3YDqM_keyframes.md) | 2026-09-24 |
| [OpenAI早見槍擊警訊卻未報警【AI新聞快報 2026/09/24】](data/ai-note-101/ai-note-101_Zeo8W6DFN5w_keyframes.md) | 2026-09-23 |
| [AlphaGo 之父為什麼刷掉祖克柏、拒絕馬斯克，把 DeepMind 賣給 Google【AI 大人說】](data/ai-note-101/ai-note-101_3NyNdSTxKEY_keyframes.md) | 2026-09-09 |
| [Meta 兩個月前拿走你的 IG 照片，現在 Meta 要你的信箱和信用卡【AI新聞快報 2026/09/10】](data/ai-note-101/ai-note-101_BAFKKutYubU_keyframes.md) | 2026-09-09 |
| [一通電話就能接管你的微信，一家紅隊公司用 AI 兩天寫出這個攻擊碼【AI新聞快報 2026/09/09】](data/ai-note-101/ai-note-101_Y40cCdonmls_keyframes.md) | 2026-09-09 |

### [富邦證券](data/fubonsec/)

> 富邦證券官方 YouTube 頻道
> 📢依據投資人需求、提供優質影音內容🔥🔥🔥
> 📢支持本頻道推出優質內容！歡迎【訂閱頻道】或【線上開戶】享手續費超優惠👉 https://fbstw.link/52Fubon
> 👍投資心法 - 周冠男教授、陳嬿如教授...等專家分享獨家投資心法！
> 👍交易指南 - 透過影音、輕鬆學會股市交易的必知指南！
> 👍產業趨勢 - 與富邦投顧合作的產業專題報告！輕鬆掌握投資趨勢！
> 👍程式交易 - 富證專家免費分享 40 堂課程，讓您零基礎學會程式交易！
> 👍平台操作 - 股票下單APP「富邦AI PRO」、「富邦e點通」快速上手！
>
> 🎬訂閱 富邦證券 YouTube 頻道、隨時掌握投資訊息！
> © 富邦綜合證券股份有限公司
> 服務信箱：service.sec@fubon.com
> 許可證字號：112年金管證總字第0020號
> 服務專線：0800-073-588
> 總公司地址：台北市大安區仁愛路四段169號3、4樓

| 影片 | 日期 |
| --- | --- |
| [半導體股估值怎麼看？從獲利成長到AI供應鏈輪動｜國泰投信李翰林 專訪](data/fubonsec/fubonsec_plZIvZ5US7E_keyframes.md) | 2026-09-30 |
| [退休規劃何時開始才不嫌晚？政大教授分享退休前15年的準備關鍵｜陳嬿如專訪 EP11](data/fubonsec/fubonsec_hj19DKuHxbQ_keyframes.md) | 2026-09-23 |
| [繼承到股票就能全部賣掉？存股族一定要懂的信託安排｜蘇家宏專訪 EP3](data/fubonsec/fubonsec_324i3yZuBLo_keyframes.md) | 2026-08-28 |
| [AI會取代你的工作嗎？數位轉型專家揭4大關鍵能力｜《今天不聊股票》詹文男專訪](data/fubonsec/fubonsec_cdsJ6wyuULM_keyframes.md) | 2026-08-26 |
| [股票存到3000萬就該規劃？遺囑、贈與、信託差異一次看懂｜蘇家宏專訪 EP2](data/fubonsec/fubonsec_EIOQDXWEZbU_keyframes.md) | 2026-08-21 |
| [CoPoS百家爭鳴：先進封裝的挑戰與投資機會｜富邦投顧 劉立中 協理《富邦說趨勢》 EP 93](data/fubonsec/fubonsec_0L7DV-hnWmM_keyframes.md) | 2026-08-19 |
| [你的股票最後會留給誰？律師揭存股族最容易忽略的財產傳承觀念｜蘇家宏專訪 EP1](data/fubonsec/fubonsec_W_cLHLRD1m8_keyframes.md) | 2026-08-14 |
| [AI零組件漲價潮再起？下半年受惠產業與ETF一次掌握｜富邦投顧 陶治瑋 副總《富邦說趨勢》 EP 92 eT富攻略](data/fubonsec/fubonsec_DfN9yS3xkuU_keyframes.md) | 2026-08-12 |
| [破解股市利空虛實：台股已從反彈走向反轉？｜富邦投顧 陳奕光 董事長《富邦說趨勢》 EP 91](data/fubonsec/fubonsec_-KLEA_c88xI_keyframes.md) | 2026-08-07 |
| [富邦證券授信開戶四合一](data/fubonsec/fubonsec_mhIgas9TsMU_keyframes.md) | 2026-08-06 |
| [AI投資新選擇！KOSPI 50如何一次掌握韓國50大企業？\| 富邦Global Sight EP10](data/fubonsec/fubonsec_ehESBhQSWyM_keyframes.md) | 2026-08-05 |

### [Jim AI Notebook](data/jimainotebook/)

> 我是 Jim，這裡是我的 AI 筆記本。
>
>   起源是現今每天有太多大多最新的 AI 技術、概念、工具、論文、產業動態，所以建立了一個全自動的AI來自動抓住重點做影片，不用自己翻獨大量資訊。分享出來給大家一起共同學習。

| 影片 | 日期 |
| --- | --- |
| [賽局理論：眼前划算，不等於長期划算｜混合策略｜逆向歸納｜Yale 公開課｜ECON159｜中集](data/jimainotebook/jimainotebook_kfPGulrqVtI_keyframes.md) | 2026-09-29 |
| [賽局理論：你的最好，取決於別人｜納許均衡｜囚徒困境｜中間選民｜Yale 公開課｜ECON159｜上集](data/jimainotebook/jimainotebook_RtytrLzbJ-0_keyframes.md) | 2026-09-26 |
| [15 分鐘看完 AI Engineer Conference｜開幕 keynote 篇｜巴黎](data/jimainotebook/jimainotebook_F5eZ5lr7edo_keyframes.md) | 2026-09-25 |
| [平行運算：難的不是管好，是交出去｜HBM｜ASIC｜交易式記憶體｜Stanford 公開課｜CS149｜下集](data/jimainotebook/jimainotebook_5jwAsjGaaUk_keyframes.md) | 2026-09-23 |
| [平行運算：難的不是分工，是共用｜GPU｜Spark ｜CUDA｜Stanford 公開課｜CS149｜中集](data/jimainotebook/jimainotebook_dFhknF3fAJg_keyframes.md) | 2026-09-20 |
| [平行運算：加了核心為什麼沒變快｜記憶體｜多核心｜快取｜Stanford 公開課｜CS149｜上集](data/jimainotebook/jimainotebook_7ipbnVilTDI_keyframes.md) | 2026-09-17 |
| [前沿系統：AI 如何變成真正能用的產品｜Stanford 公開課｜CS153｜下集](data/jimainotebook/jimainotebook_dttPH3QWdK0_keyframes.md) | 2026-09-15 |
| [DeepSeek V4.1 Flash，到底 Flash 在哪？](data/jimainotebook/jimainotebook_ECDoHDwhsjM_keyframes.md) | 2026-09-13 |
| [前沿系統：AI 產業的真實運轉｜Stanford 公開課｜CS153｜上集](data/jimainotebook/jimainotebook_N1eF7fCm_Hk_keyframes.md) | 2026-09-07 |
| [電腦如何理解人類語言？ 從 Embedding 說起](data/jimainotebook/jimainotebook_ata4dmLP5IU_keyframes.md) | 2026-09-02 |
| [從零開始訓練一個大型語言模型 ｜ Stanford 公開課 ｜中集](data/jimainotebook/jimainotebook_ddTy5Fra4-4_keyframes.md) | 2026-08-30 |

### [LEI](data/lei/)

> 老雷｜投資人
>
> 我在投資上追求兩個目標：
> 1. 尋找市場規律，因為規律可以重複利用。
> 2. 賺最容易賺到的錢，讓錢為我工作。
> 如果你的目標與我相同，那麼我的經驗和思考就可以為你所用了。
>
> As an investor, I focus on two goals:
> 1. Discovering market principles that can be applied repeatedly.
> 2. Capturing the easiest opportunities to make money, letting my money work for me.
> If your goals are similar, my experiences and insights may be useful to you.

| 影片 | 日期 |
| --- | --- |
| [【硬核】我用二十年經驗總結的投資分析框架](data/lei/lei_qbU7LHPZ4Xo_keyframes.md) | 2025-11-27 |

### [Smart智富月刊](data/smartmonthly-bw/)

> 《Smart智富》成立於1998年，提供股票、基金、期權、黃金、外幣、債市、房地產、保險、退休規劃、消費觀念等投資理財領域的知識、情報與課程服務。旗下產品有台灣發行量最大的理財月刊－《Smart智富》月刊、排行榜常勝軍－《Smart智富》密技雙月刊、《平民股神教你不蝕本投資術》《權證小哥教你十萬變千萬》等財經暢銷書，以及DVD、課程講座、大型論壇、facebook等，全方位服務投資族群需求。
>
> Smart自學網 http://smart.businessweekly.com.tw/
> 商周Smart課程好學 https://smart.businessweekly.com.tw/ecourse/index.aspx
> 《Smart智富》月刊粉絲團 https://www.facebook.com/smartmonthly

| 影片 | 日期 |
| --- | --- |
| [AI股獲利了結後，錢可以擺在哪裡? 帶您關注『潛力市場』的配置機會｜詹璇依、黃大展│Smart投資教室](data/smartmonthly-bw/smartmonthly-bw_opHWowpsGA8_keyframes.md) | 2026-09-30 |
| [央行第7波信用管制滿兩週年，成屋買氣有感回溫？｜永慶房屋陳賜傑、Amy｜房產關鍵字](data/smartmonthly-bw/smartmonthly-bw_HLeipjrNbik_keyframes.md) | 2026-09-29 |
| [FED還會升息幾次？利率會升到多高？台股何時可能反轉？造成通膨失控的潛在危機是什麼？｜峰哥｜Smart智富．投資的一千零一夜252](data/smartmonthly-bw/smartmonthly-bw_V35DrgT3U7w_keyframes.md) | 2026-09-26 |
| [韓國就是狂，8月出口年增近70%，營業利益上攻1,000兆韓圜，三星獲利比肩輝達｜仲葳｜Smart投資教室](data/smartmonthly-bw/smartmonthly-bw_pItgJoTM7DA_keyframes.md) | 2026-09-25 |
| [台股創新高就能追？別急！追強不追高，慎防假突破｜王子縈、佑佑｜理財佑佑班](data/smartmonthly-bw/smartmonthly-bw_tFVq0jnAq0M_keyframes.md) | 2026-09-22 |
| [台股還能投資？AI商機多點開花，市值型ETF 2.0掌握「現任＋下任」核心｜璇依、峰哥｜人人都能學會ETF](data/smartmonthly-bw/smartmonthly-bw_Q6T7rLcSbds_keyframes.md) | 2026-09-21 |
| [台股5萬點只是前菜？杜金龍：這波牛市末升段上看8萬點！台積電有機會漲到哪裡？杜大師解密台積電、聯發科與鴻海實戰操作心法！｜峰哥ft. 杜金龍｜Smart智富．投資的一千零一夜251](data/smartmonthly-bw/smartmonthly-bw_LKAYiw41EZg_keyframes.md) | 2026-09-19 |
| [韓股去槓桿結束，反攻號角可能正要吹響 ｜仲葳｜Smart投資教室](data/smartmonthly-bw/smartmonthly-bw_WXZqPbEusDA_keyframes.md) | 2026-09-18 |
| [越南股市2025年漲幅超過4成*！這只是剛開始嗎？「越南2.0」5大升級看未來10年｜峰哥、中國信託越南機會基金經理人張晨瑋｜Smart投資教室](data/smartmonthly-bw/smartmonthly-bw_YoNKzSvLxj8_keyframes.md) | 2026-09-18 |
| [黃仁勳出手1000億，圖什麼？聯發科與供應鏈迎最大商機，產業隊長張捷點名供應鏈受惠股，下一批飆股曝光！｜峰哥ft. 張捷｜Smart智富．投資的一千零一夜250](data/smartmonthly-bw/smartmonthly-bw_fR7auIG3M-0_keyframes.md) | 2026-09-12 |
| [越南正夯！股怪教授解析投資機會ｘ越南美女帶路吃喝玩樂！｜詹璇依、股怪教授謝晨彥、Hang TV越南夯台灣頻道主阮秋姮｜Smart投資教室](data/smartmonthly-bw/smartmonthly-bw_NgXyMZaZbfQ_keyframes.md) | 2026-09-07 |
| [升息、強美元、AI股大舉債，當心可能推倒台股的三塊骨牌！｜峰哥｜Smart智富．投資的一千零一夜249](data/smartmonthly-bw/smartmonthly-bw_OunGyJJy9x8_keyframes.md) | 2026-09-05 |
| [清大5000萬變50億！操盤人林哲群公開「賺錢的方法」。50歲有一筆錢，怎麼投資？小資族如何從小錢開始累積資產？清大校務基金現在的持股組合？｜峰哥ft. 林哲群｜Smart智富．投資的一千零一夜248](data/smartmonthly-bw/smartmonthly-bw_TrzuopEcNDE_keyframes.md) | 2026-08-29 |
| [好公司跌破支撐該跑還是加碼？別無腦加！先看估值，跌深不等於便宜｜雷浩斯、佑佑｜理財佑佑班](data/smartmonthly-bw/smartmonthly-bw_QDPTr7wipx8_keyframes.md) | 2026-08-25 |
| [客戶叫我「土下座」！雪寶揭外匯交易職涯最震撼的一天。國外旅遊遇搶，雪寶竟然這樣回搶匪？雪寶最想問峰哥的兩個理財問題是什麼？｜峰哥ft. 雪寶｜Smart智富．投資的一千零一夜247](data/smartmonthly-bw/smartmonthly-bw_WzJjPd3iG0M_keyframes.md) | 2026-08-22 |
| [連味精都能壟斷AI！看懂日企憑什麼掌控全球命脈？｜曾仲葳、CFP®國際理財顧問吳盛富｜Smart投資教室](data/smartmonthly-bw/smartmonthly-bw__FsaTDrvsms_keyframes.md) | 2026-08-18 |
| [高檔賣7成、低檔全買回，投資達人雷浩斯持股衝95%，他看好那些標的?｜峰哥ft. 雷浩斯｜Smart智富．投資的一千零一夜246](data/smartmonthly-bw/smartmonthly-bw_5wLmS5-slJY_keyframes.md) | 2026-08-15 |
| [日圓甜甜價沒了，28年首見！美日聯手救日圓，下一場股災要來了？新台幣怎沒跟著日圓升值？｜峰哥｜Smart智富．投資的一千零一夜245](data/smartmonthly-bw/smartmonthly-bw_-3z0BSuQ9p8_keyframes.md) | 2026-08-08 |
| [暴漲暴跌怎麼做當沖？選股竟不看K棒！股價、成交值、大戶單為關鍵｜林昇、佑佑｜理財佑佑班](data/smartmonthly-bw/smartmonthly-bw_XG6az-eXZNY_keyframes.md) | 2026-08-06 |
| [AI股危機不是獲利下滑，而是自由現金流正在消失。哪些熱門ETF受創最大？0050比較抗震嗎？｜峰哥｜Smart智富．投資的一千零一夜244](data/smartmonthly-bw/smartmonthly-bw_WW1Kpl3LLc0_keyframes.md) | 2026-08-01 |
| [吃播聊投資，峰哥怎麼看債券ETF？長期資金，選0050或台積電？市場反彈，佑佑加碼部位的資產翻正了嗎？｜佑佑，峰哥｜人人都能學會](data/smartmonthly-bw/smartmonthly-bw_XcMUo9k65Rs_keyframes.md) | 2022-11-29 |

### [LEI](data/themarketmemo/)

> 老雷｜投資人
>
> 我在投資上追求兩個目標：
> 1. 尋找市場規律，因為規律可以重複利用。
> 2. 賺最容易賺到的錢，讓錢為我工作。
> 如果你的目標與我相同，那麼我的經驗和思考就可以為你所用了。
>
> As an investor, I focus on two goals:
> 1. Discovering market principles that can be applied repeatedly.
> 2. Capturing the easiest opportunities to make money, letting my money work for me.
> If your goals are similar, my experiences and insights may be useful to you.

| 影片 | 日期 |
| --- | --- |
| [破解投資圈「窮人思維模式」](data/themarketmemo/themarketmemo_tNzUUET5opY_keyframes.md) | 2026-01-16 |
| [全職投資人，需要具備哪些條件？](data/themarketmemo/themarketmemo_hDOZ5n9PJFI_keyframes.md) | 2025-12-03 |
| [【硬核】我用二十年經驗總結的投資分析框架](data/themarketmemo/themarketmemo_qbU7LHPZ4Xo_keyframes.md) | 2025-11-27 |
| [市場崩盤的本質是什麼？｜聊聊流動性風險](data/themarketmemo/themarketmemo_IMZgGZVQu2M_keyframes.md) | 2025-10-09 |
| [我的故事：從設計師到職業投資人](data/themarketmemo/themarketmemo_DRiYHzY83T0_keyframes.md) | 2025-10-01 |

### [財訊](data/wealth1974/)

> 1974年創刊的《財訊》，是台灣財經雜誌中，最資深權威的財經專業媒體。
>
> 數十年來始終秉持「引領趨勢、創造財富，掌握政經、放眼國際」的核心價值，
> 報導領域涵蓋財經趨勢、投資資訊、企業動向、產業動態、政情研判等，
> 是創造兩岸三地政經投資理財議題，洞燭市場的先行者。
>
> 在 2009年10月28日，《財訊》正式改版為《財訊雙週刊》，
> 更迅速的反映新聞的變化、更及時地為讀者篩選出真正有用的資訊。
>
> 一如月刊般嚴謹的查證，追蹤深入報導新聞始末，既有月刊的深度，也具有周刊的速度！
> 除了既有的財經及政治深入報導之外，還有更多金融訊息與投資含量，提供讀者更專業、更豐富、更實用的財經資訊。
>
> 《財訊雙週刊》開闢企業、投資、金融、政治、科技等不同領域的重量級名人專欄，
> 由中外名家：諾貝爾大師史迪格里茲、謝金河、陶冬、南方朔、吳念真、顧爾德、林昭亮等輪流執筆，提供專業新知與獨到見解。
>
> 同時精選全球財經專業媒體的授權文章，
> 透過英國《金融時報FINANCIAL TIMES》、
> 美國《華爾街日報THE WALL STREET JOURNAL》、
> 日本《朝日新聞》，提供讀者更多元且深入的國際視野。
>
> 近年更致力於數位化閱讀，電子雜誌、手機格式、線上閱讀等，
> 與平面雜誌同步發行，期許更貼近讀者生活、資訊流通更迅速即時。
>
> 【免責聲明】
> 《財訊》盡力提供精準之資訊分享予投資人參考，資訊內容不保證絕對無誤，投資人應獨立判斷，審慎評估並自負投資風險及盈虧。
> 您因參考本頻道所分享之內容而進行之任何投資或特定目的行為，所產生之任何直接、間接、附帶或因而導致或衍生之各項損失，皆應由您自行承擔，《財訊》概不負責。
> 《財訊》所提供之投資分享，只可作為參考之用，並不構成要約、招攬、邀請、誘使、任何不論種類或形式之申述或訂立任何建議及推薦，投資人應自行判斷與承擔風險。

| 影片 | 日期 |
| --- | --- |
| [高利率時代的資產配置 靠一關鍵突破升息逆風！｜#聽了財知道 EP373 #升息 #聯準會](data/wealth1974/wealth1974_mPb3BC9Z1OM_keyframes.md) | 2026-09-30 |
| [獨家揭露 台積電麥寮外海的秘密計畫｜#聽了財知道 EP372 #碳封存 #台積電](data/wealth1974/wealth1974_JkQcyPHusrA_keyframes.md) | 2026-09-28 |
| [台股市值躍升全球第四大 政府應該思考的下一步｜#老謝開講 EP294 #財訊](data/wealth1974/wealth1974_tpUuNwcWiFU_keyframes.md) | 2026-09-25 |
| [【會員影片節選】AI 晶片測試火熱 八檔受惠股旺到明年｜ #產業投資通 EP04 #半導體測試 #探針卡](data/wealth1974/wealth1974_qL5ms5oowHA_keyframes.md) | 2026-09-24 |
| [欣興案示警 台廠小心誤踩供應鏈紅線｜#聽了財知道 EP371 #欣興](data/wealth1974/wealth1974_yN2CYvg11QA_keyframes.md) | 2026-09-23 |
| [五大商社砸重金 尋找下個成長動能｜#投資IN總經 EP97  #財訊 #日本](data/wealth1974/wealth1974_GIVExayTQwM_keyframes.md) | 2026-09-22 |
| [台積電領頭 四大亮點引爆 AI 新格局｜#聽了財知道 EP370 #SEMICON #台積電](data/wealth1974/wealth1974_ksWBCvgQR5k_keyframes.md) | 2026-09-21 |
| [三現象拆解生技熱 漲升內涵大不同｜#財訊不漏接 EP053 #財訊podcast #捷立康 #康霈 #仁新](data/wealth1974/wealth1974_kDBwZJ7kMxQ_keyframes.md) | 2026-09-19 |
| [台灣下一座護國神山？ 健康產業將有億元市場｜#老謝開講 EP293 #財訊 feat. 威力先進董事長 王文欽](data/wealth1974/wealth1974_c68PvMZYzOo_keyframes.md) | 2026-09-18 |
| [機器人走向量產 能改善醫護負擔嗎？｜#幸福經濟學 EP16 #財訊](data/wealth1974/wealth1974_5gxEt8Vgtiw_keyframes.md) | 2026-09-17 |
| [【會員影片節選】AI 訂單讓台廠大賺錢 但卻缺自由現金｜#聽了財知道 EP364 #鴻海 #緯穎](data/wealth1974/wealth1974_JOLqghWExO8_keyframes.md) | 2026-08-31 |

### [X的財經筆記](data/x/)

> 經濟分析｜投資策略 | 人生智慧

| 影片 | 日期 |
| --- | --- |
| [巴菲特&芒格：社会运行的本质，它会奖励哪些人！#charliemunger #投資 #投資心法 #warrenbuffett  #芒格  #巴菲特](data/x/x_nNtdo6Lsop4_keyframes.md) | 2026-07-30 |
| [巴菲特：停止改变别人把全部能量用来投资自己！#charliemunger #投資 #投資心法 #warrenbuffett  #芒格  #巴菲特](data/x/x_vF4QvcDmWIs_keyframes.md) | 2026-07-29 |
| [芒格：遠離這三類人，你的人生才會開掛！ #charliemunger #芒格](data/x/x_SE5CoXNuG_Y_keyframes.md) | 2026-06-14 |
| [查理·芒格：人生漫長，充滿了遺憾和痛苦！#charliemunger #芒格](data/x/x_WozyR-uRgUs_keyframes.md) | 2026-06-13 |
| [既然巴菲特的持倉是公開的，我們為什麼不能跟著買？#warrenbuffett #投資 #巴菲特](data/x/x_vlDErtgEyFM_keyframes.md) | 2026-06-12 |
| [投资方法论与决策科学｜风投女神徐新投资中的三个方法论](data/x/x_dzTP-abkWCc_keyframes.md) | 2026-02-11 |
| [告別複雜公式！巴菲特估值法核心就一條！](data/x/x_Ofio1iI-i50_keyframes.md) | 2025-12-01 |

### [游庭皓的財經皓角](data/yutinghaofinance/)

> 游庭皓，財經作家、投資人。清華大學經濟學學士，台灣大學法學碩士，曾任投信投顧研究員，具投信投顧證照，經濟日報、聯合晚報、智富月刊、Money錢撰稿人，研究方向以總體經濟變化與景氣週期投資為主。
>
> 著有：《股債雙存獲利六堂課》
>
> 大家好，我是庭皓，股齡十年，現在依然在實現財務自由的道路上，按照目前的投報率與本業收入，我將會在2025年前，達到財務自由，並辭去所有工作，把時間專注在本網站，以及我更熱愛但收入不確定的事業。
>
> 您可能會好奇，怎麼會是由一個連自己都還未財務自由的人，來教導我們財務知識呢？
>
> 我是這樣想的，多數成功者，都是在取得成功後，才把榮耀、結果展現在他人面前，但這對投資人毫無幫助，因為這種成功，可以刻意的去剪裁，忽略或隱藏，使我們盲目的崇拜，卻不知如何下手。
>
> 於是，我決定將這件事反過來，我無法保證五年內一定財務自由，但我也不願在成功後才刻意剪裁，所以，在本網站介紹的投資策略，不是我成功後，刻意拼接的成功論，而是實在的方法論。
>
> 我希望在接下來的時間，與各位一起成長，在很多年後，我們可以有底氣的說：
>
> 這就是我們的計劃，我們就是按照這項計劃，一步一步的實現財務自由。
>
> 2019/11/21 台北

| 影片 | 日期 |
| --- | --- |
| [2026/10/1(四)美股詭異行情!債市拉警報 基本面卻上修?八成個股下跌 AI能撐多久?【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_FsIraI_ezPI_keyframes.md) | 2026-10-01 |
| [2026/9/30(三)利率越漲 美股越不跌？數兆美元豪賭 AI驗收期到了嗎?【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_eHz1_TGAo4I_keyframes.md) | 2026-09-30 |
| [2026/9/29(二)10年美債殖利率 升破5.2%!債市會把股市 拖下水嗎?【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_wBb7G4Ifd34_keyframes.md) | 2026-09-29 |
| [2026/9/23(三)5%殖利率也擋不住FOMO？AI狂潮推那指再創新高【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_Xlj2cBFC7_s_keyframes.md) | 2026-09-23 |
| [2026/9/22(二)那指創新高!個股沒跟上?美股重新押注AI 不怕高利率了？【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_U4RH_CPe3GQ_keyframes.md) | 2026-09-22 |
| [2026/9/21(一)美股最危險組合:油價100美元+美債5% 川習會登場 利多還有戲?【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_EJdsmRgakkU_keyframes.md) | 2026-09-21 |
| [2026/9/18(五)台灣央行 為何不升息?第2戶貸款回7成 房市底部到了?【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_Ulz539c38mw_keyframes.md) | 2026-09-18 |
| [2026/9/17(四)三年首度升息!這只是剛開始?升息循環開啟 美股漲得動嗎?【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_TQ_oEc9vnB8_keyframes.md) | 2026-09-17 |
| [2026/9/16(三)股市還在撐 債市先崩?2026最難一局 Fed升息後 誰先投降？【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_wmu1GS07BMo_keyframes.md) | 2026-09-16 |
| [2026/9/15(二)AI踩煞車 重擊晶片股?10年債殖利率破5% AI泡沫洩氣？【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_KNWS5tp0HYc_keyframes.md) | 2026-09-15 |
| [2026/9/14(一)油價破百!升息箭在弦上?中期選舉倒數 美債撐得住?【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_FtPa8H718To_keyframes.md) | 2026-09-14 |
| [2026/9/11(五)油價破百 債券失火!股市撿便宜?【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_mhVVuuWUhCw_keyframes.md) | 2026-09-11 |
| [2026/9/10(四)摺疊機登場 蘋果救美股? 市場飽和 蘋果能創造 下一個換機潮？【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_cOTLqoaHBxE_keyframes.md) | 2026-09-10 |
| [2026/9/9(三)油價快破100美元 期中選舉拉警報?道瓊跌費半升!市場大換血?【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_b2MbRUsIaU8_keyframes.md) | 2026-09-09 |
| [2026/9/8(二)亞幣大升值 錢往亞洲跑  外資回補潮?台灣擴廠潮 游資擋不住!【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_O0JBTLUGnQ0_keyframes.md) | 2026-09-08 |
| [2026/9/7(一)非農超強 美債失守 AI股卻悄悄轉多?美股Q4還有戲?【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_c4IT1Mwb_Pg_keyframes.md) | 2026-09-07 |
| [2026/9/4(五)沒人接盤 債市要變天?2027兆元帳單來了 美股內部出現裂痕?【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_6weg9-YmGVs_keyframes.md) | 2026-09-04 |
| [2026/9/3(四)美國製造業 真的回來了？台灣央行 該升息了嗎?【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_R15MWKzLJpE_keyframes.md) | 2026-09-03 |
| [2026/9/2(三)高利率炸彈 AI還能撐?亞洲AI行情 迎來大考驗?【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_fpX071E5yI4_keyframes.md) | 2026-09-02 |
| [2026/9/1(二)美伊再交火 巨頭續燒錢！美股能擺脫 九月魔咒嗎?【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_XY31kO-V0Q4_keyframes.md) | 2026-09-01 |
| [2026/8/31(一)華許放鷹 升息躲得掉?高利率越久 美債美股 誰先撐不住？【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_BxtHhc6P1n0_keyframes.md) | 2026-08-31 |
| [2026/8/28(五)輝達救美股 華許救美債?台灣景氣連八紅 台灣人終於有感?【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_rTnPsm_gAhA_keyframes.md) | 2026-08-28 |
| [2026/8/27(四)輝達財報再超標!追高意願低?美股為何原地踏步?【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_lDeHFopOfIs_keyframes.md) | 2026-08-27 |
| [2026/8/26(三)美債回購能 救川普選情?日本缺工 歐洲缺膽 誰能突圍?【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_KUZC2NyCCCY_keyframes.md) | 2026-08-26 |
| [2026/8/25(二)輝達連七黑 領頭羊動搖 ?經濟諾曼第行動 通膨撐得住?【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_tLvKGHyxhd8_keyframes.md) | 2026-08-25 |
| [2026/8/24(一)美債救不動 黃金 比特幣先起飛?關稅戰再起 最後誰買單？【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_dFYqrIQIMvw_keyframes.md) | 2026-08-24 |
| [2026/8/21(五)巨頭搶錢 誰來接美債?AI是革命or下一場債務危機?【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_ajjRvohk-Og_keyframes.md) | 2026-08-21 |
| [2026/8/20(四)貝森特護盤!美債有救了?巨頭燒錢換市佔 利息拖垮經濟?【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_LUGWERSl01s_keyframes.md) | 2026-08-20 |
| [2026/8/19(三)債市風暴 撿便宜時刻?美中爭霸燒錢戰 Al時代只能二選一？【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_9VqNpjPGmbM_keyframes.md) | 2026-08-19 |
| [2026/8/18(二)美股買盤停止追高 散戶等回檔?台灣游資氾濫 普發成常態?【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_aRPmzQfTLFc_keyframes.md) | 2026-08-18 |
| [2026/8/17(一)指數創高 回檔等加碼?美課100%關稅 無人機大戰開打!【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_OJ5vxmwQrE0_keyframes.md) | 2026-08-17 |
| [2026/8/14(五)AI股不再雞犬升天 債市開始算帳!AI帳單 誰會來買單?【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_oLPxNHRAPEI_keyframes.md) | 2026-08-14 |
| [2026/8/13(四)通膨退一步 股市進兩步?情緒轉彎 槓桿資金回來了?【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_KS_BkfqfALI_keyframes.md) | 2026-08-13 |
| [2026/8/12(三)GPU金融化狂潮 2008正在重演？兆元商機還是下一場危機？【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_ApykW90PQ58_keyframes.md) | 2026-08-12 |
| [2026/8/11(二)AI舉債時代 自由現金流能翻正?外資再加空單!台股還能攻?【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_v7TpiWK5DTQ_keyframes.md) | 2026-08-11 |
| [2026/8/10(一)非農爆冷 升息機率降?美股創高!波克夏也開始買股了?【早晨財經速解讀】](data/yutinghaofinance/yutinghaofinance_5_poweJsVBA_keyframes.md) | 2026-08-10 |

## 目錄慣例
```
data/{channel}/{channel}_{video_id}_GT.srt   # 人工校正後的 ground truth（單一真相來源）
data/{channel}/{channel}_{video_id}_FIN.srt  # pipeline 依 CER 挑選出的最終逐字稿
```
`video_id` 為固定 11 碼的 YouTube 影片 ID；stem = `{channel}_{video_id}`。

## 使用方式

1. 複製 `.env.example` 為 `.env`，填入 GitHub PAT 與 repo 設定
2. （可選）用 `skill-youtube-channel-fetch` 自動從頻道抓最新影片音訊並寫入
   `audio_manifest.json`；也可手動在 `audio_manifest.json` 加入 `{stem: audio_url}`
   （格式範例見 `audio_manifest.example.json`）：
   ```bash
   pip install -r requirements.txt
   python skills/skill-youtube-channel-fetch/scripts/channel_fetch.py fetch \
       https://www.youtube.com/@fubonsec --limit 5
   ```
   也可以指定日期區間，抓某段期間內的所有影片（而非「最新 N 支」）：
   ```bash
   python skills/skill-youtube-channel-fetch/scripts/channel_fetch.py fetch \
       https://www.youtube.com/@yutinghaofinance --date-after 2026-08-01 --date-before 2026-08-07
   ```
3. 觸發轉錄：
   ```bash
   python skills/skill-mlx-api-client-whisper/scripts/whisper_issue_client.py sync audio_manifest.json
   ```
   對每個尚未有 `FIN.srt` 的 stem，會在 `WHISPER_TARGET_REPO`（Mac-mini repo）開一張
   `generate-FIN` issue 觸發轉錄；已完成的 stem 則自動關閉對應 issue。
   （步驟 2 加 `--sync` 可以合併這一步。）
4. 若某支影片的 `GT.srt` 被人工修正過，想讓 pipeline 重新評分（不重新轉錄），呼叫
   `open_fin_request(stem, audio_url, task_type="refine_fin_srt")`（見 skill SKILL.md）。
5. 有 `FIN.srt` 後，用 `skill-youtube-channel-srt-keyframe-extract` 分析逐字稿找出圖表／簡報等
   視覺重點時刻，擷取對應畫面存成帶時間碼的 PNG：
   ```bash
   python skills/skill-youtube-channel-srt-keyframe-extract/scripts/keyframe_extract.py extract <stem> \
       --srt data/<channel>/<stem>_FIN.srt \
       --video-url https://www.youtube.com/watch?v=<video_id>
   ```

## 自動化（每日排程）

`.github/workflows/daily-channel-fetch.yml` 每天自動：

1. 對 `channels.json` 裡列的每個頻道跑 `channel_fetch.py fetch <url> --limit 5 --sync`，
   抓新影片、寫逐字稿/manifest、觸發 whisper
2. 對每個「有 `FIN.srt`（沒有的話退而求其次用 `GT.srt`）但還沒有 `_keyframes.md`」的
   stem 跑 `skill-youtube-channel-srt-keyframe-extract`，補齊關鍵畫面擷取（每支重試一次；
   YouTube 端偶發限流導致某支失敗不會擋住其他支，會留到隔天的排程自動重試，因為判斷條件
   就是「還沒有 `_keyframes.md`」）
3. 重新產生 README「內容索引」並 commit——新影片跑完關鍵畫面擷取後就會自動出現在這裡

也可用 `workflow_dispatch` 手動觸發並自訂 `limit`。要追蹤新頻道，直接編輯 `channels.json`
加一行 URL 即可，不用改 workflow。

此 workflow 需要在 repo 的 GitHub Actions Secrets 設定：
- `YOUTUBE_COOKIES_B64`：YouTube cookies.txt 內容的 base64 編碼；給 `yt-dlp` 通過
  YouTube「Sign in to confirm you’re not a bot」檢查用
- `REPO_FILE_SYNC_WENCHIEHLEE_MONEY`：對本 repo `Contents: Read and write`（發布音訊 Release、
  push commit）
- `REPO_FILE_SYNC_ZHONGZHENG782_MONEY`：對 `WHISPER_TARGET_REPO`（Mac-mini repo）
  `Issues: Read and write`（`--sync` 觸發轉錄用）
- `GEMINI_API_KEY`、`CODEX_API_URL`、`CODEX_API_KEY`：關鍵畫面擷取要判斷「哪些時間點值得
  截圖」時呼叫的 `llm` 套件 provider 憑證（`../llm` 的 codex → gemini → mlx 備援鏈；CI
  環境連不到僅限內網/Tailscale 的 `MLX_API_URL`，所以沒設 mlx 相關 secrets，鏈路會直接
  落到 codex/gemini 其中之一）

手動字幕來源、只有 `GT.srt` 沒有 `FIN.srt` 的 stem，也會照常被拿去做關鍵畫面擷取（找不到
`FIN.srt` 時改用 `GT.srt` 當來源）——截圖跟逐字稿片段仍然有效，之後若跑了 `refine` 讓
Mac-mini pipeline 產出正式版 `FIN.srt`，可以再手動重跑一次關鍵畫面擷取讓內容更新。

## Podcast 訂閱（`scripts/generate_podcast_feed.py`）

每個有音訊（Release asset）的頻道都會產生一份獨立 RSS feed（`docs/{channel}/feed.xml`），
可在 Apple Podcasts / Overcast / Pocket Casts 等 app 用「Add by URL」訂閱：

```
https://zhongzheng782.github.io/YoutubeAudio.Fetch/{channel}/feed.xml
```

不想每個頻道分別訂閱的話，也有一份跨所有頻道合併的單一 feed：

```
https://zhongzheng782.github.io/YoutubeAudio.Fetch/feed.xml
```

合併 feed 裡每一集的標題會加上 `【頻道名稱】` 前綴，並附上該集專屬的關鍵畫面縮圖當封面
（`<itunes:image>`，各家 app 清單上會顯示不同縮圖）、以及 `<itunes:author>` 標示來源頻道，
方便在同一份清單裡分辨集數來自哪個頻道。兩種 feed 都由每日排程的最後一步
（`scripts/generate_podcast_feed.py <channel>` / `--all`）自動重新產生。

## 詳細設計

issue metadata schema、stem 解析規則、company-configs 調校/GT 校正迴圈見
`Mac-mini` repo 的 `skills/skill-mlx-api-server-whisper/SKILL.md`。
