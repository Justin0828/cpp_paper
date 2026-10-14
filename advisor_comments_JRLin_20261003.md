# 导师批注对照清单

来源：`cpp_paper_english-20261003JRLin.pdf`（批注作者 jiaru，2026-10-03）。

后续改论文以本清单的编号为准。批注原文照录，包括个别疑似笔误。第 2、19、27、28 页没有导师批注。同一处的高亮和便签、删除和替换已合并。

每条的「处理」取值：

- `直接改`：批注已经写明改法，照做。
- `按意图改`：批注本身不清楚。下面的「意图」是根据上下文做的猜测，「改法」是据此准备采用的修改。作者不提出异议，就按改法改。
- `按方案改`：批注方向清楚，但改写幅度大。下面的「方案」是准备采用的修改。作者不提出异议，就按方案改。
- `待定`：批注方向清楚，但改写幅度大，或还要作者选方案；这里没有另写默认改法。
- `已改`：正文已经按本条改完。

## 第 1 页 · 标题和摘要

**1.** 划中标题 “Coverage Path Planning for a Swing-Arm Concrete Troweling Robot in Complex Environments”。

批注：1. 挖掘一下算法特色，目前标题对算法特色和创新性的体现不足；2. 给算法或关键模块取个响亮的名字？3. 论文总体上感觉不同的概念太多，或同一事情用了不同的概念去表达，会让人看起来很累。

方案：标题改为 “BiRect: Bidirectional Rectangular Coverage Path Planning for a Swing-Arm Concrete Troweling Robot”。BiRect 只指本文这套方法，取自 bidirectional rectangular coverage；算法特色写进标题的是双向矩形分解，不再用 “Complex Environments” 充当创新点。复杂地图留在摘要的缺口句里。摘要、第 9 条的贡献句和后文第一次指这套方法时都叫 BiRect，不再并列 hierarchical CPP、proposed pipeline、our framework 等第二名称；“the proposed method” 只作回指。本轮改到的句子同时锁用词：行走本体用 base，本机抹盘用 disc，摆臂用 swing arm（定语 swing-arm），规划结果用 route，带时间的基座–摆臂运动用 trajectory。tool 只泛指 CPP 机具，path 只保留在 CPP 这个术语里。不顺手改本条没有点名的段落，后面各条再按同一用词改。
处理：按方案改

**2.** 划中摘要开头整段，从 “Concrete floor troweling must cover large areas...” 到 “...generate a continuous, executable route in a complex map.”

批注：思路优化和适当压缩。一种思路是：摆臂机器人相较……在完成大量、重复性混凝土抹平工作中具有显著优势。然而，既有算法仍聚焦……，缺乏对……的考虑。因此，本研究提出……

方案：摘要开头三句按这个节拍重写，不比现在更长，也不把引言里的安全、硅尘和工时窗口搬进摘要。第一句：相较 center-mounted 和 front-mounted，摆臂机器人在大面积、重复性抹平中能让基座躲开墙、柱和孔洞，同时由抹盘覆盖侧向和窄区。第二句：既有 CPP 仍聚焦规则场地或农田里的固定工具足迹，没有考虑主动摆臂，也没有考虑复杂地图上抹盘的时变扫掠。第三句接 “This paper therefore presents BiRect”，后面的贡献句按第 3 条写。优势只列这两点，和第 12 条用同一组，不另写有效宽度公式。
处理：按方案改

**3.** 贴在贡献句 “organizes the workspace using axis-aligned rectangular candidates...” 旁边，没有单独划线。

批注：论文贡献和成果的写法：提出了……，引入了……，开发了……。目前的写法太平了，看不出我们的贡献或成果。

方案：删掉 “The method first ... It then ...” 这两句平铺。BiRect 引出后连用三个动词，每句一件事。提出：面向已知二维障碍地图，把复杂自由空间上的访问顺序和基座–摆臂协同运动接成一条可执行 route。引入：双向矩形候选，加上补洞和连通补全，使不规则自由空间成为摆臂能连续访问的矩形。开发：随臂角变化的局部摆扫；覆盖率和执行时间按圆盘沿完整轨迹的实际扫掠计算，车速与摆臂角速度的耦合作用对扫掠连续性和工时的影响进一步得到揭示。第 5、6 条的 coupled 和 further revealed 就落在第三句里，不另起说法。不增加第四条贡献。实验句仍按第 4、7 条改，数字不改。
处理：按方案改

**4.** 划中 “On two test maps,”。

批注：Experiments showed that。

处理：直接改

**5.** 在 “while the effects of base speed and arm angular velocity” 的 “the” 和 “effects” 之间插入 “coupled”。改完是 “while the coupled effects...”。

处理：直接改

**6.** 删去 “explicitly included.”，改为 “further revealed.”。所在句是 “...on sweep continuity and execution time are explicitly included.”

处理：直接改

**7.** 删去 “on five maps”。所在句是 “Experiments on five maps further show that the bidirectional candidate strategy...”

处理：直接改

## 第 3 页 · Introduction

**8.** 划中 “[14, 15, 16, 17, 18, 19, 20]”。所在句是 “...such as agriculture in which the tool footprint is fixed [14, ...].”

批注：这种引用形式不好，建议拆分开，具体对应到哪个词或哪半句话。

方案：这串是 choset1998、gabriely2001、bahnemann2021、polygoncoverage、mier2023、fields2cover、nobleo，对应 PDF 的 [14]–[20]。删掉 respectively：原文把它写成三种做法对三种场景，但七篇文献不是按这个顺序排的。引用改贴到它支持的半句上，不新增文献。单元分解后的往复扫掠贴 Choset 和 Bähnemann；带孔多边形上的分解与转移贴 polygon coverage；栅格上的生成树遍历贴 Gabriely，Nobleo 的占据栅格覆盖也贴在这半句，不放进农业；固定宽度条带、曲率受限连接和农业场景贴 Fields2Cover 的论文与软件。同一段下一句里捆在一起的两篇也拆开：SatAOI 贴 lin2025，移动机械臂的局部运动贴 thakar2022。不改各篇文献本来的结论。
处理：按方案改

**9.** 划掉这一整段：“Bidirectional rectangular candidates and connectivity completion represent the complex free space. A feasible transition graph then organizes global visitation, and first visits and repeated transit visits are instantiated as local swing-assisted coverage motions and transfer motions, respectively. Finally, the coverage ratio and execution time are computed from the region actually swept by the circular disc along the continuous trajectory. The same robot model is thus used for map representation, arm behavior, and trajectory evaluation.”

批注：这部分可以不降，适当优化一下前面这句话，突出我们的核心贡献即可；然后跟下一段合并。

意图：「可以不降」按笔误理解成「可以不展开」。老师不是要删掉贡献，而是觉得这段把步骤又讲了一遍，和后文的结构段抢位置。
改法：介绍里 “To close this gap, this paper presents...” 改成直接写贡献：提出一套分层覆盖路径规划，把双向矩形分解、可行转移图上的访问顺序，以及按圆盘实际扫过面积计算的覆盖率和工时放在同一条链路里。被划掉的步骤段不再单独成段，只把「同一套基座–摆臂–圆盘模型贯穿地图、局部运动和轨迹评价」并进这句。紧接着就是论文结构段。
处理：按意图改

## 第 4 页 · 2.1 抹平机器人

**10.** 高亮 “The evolution of concrete-troweling equipment can be understood along two axes: the disc–base relationship and the mode of control.” 页左有一条长竖线和两支箭头，把上面的便签指到这句。

批注：先把下面这句话放到前面，然后再讲从 disc-base relationship 的角度可以分为三类，分别是……。下面那段话开头则说从 mode of control 的角度可以分为……。

方案：2.1 在抹平工艺那段之后重排，事实不改。划中的两轴句前移，作为构型讨论的第一句。下一段用 disc–base relationship 起头，按第 11 条写成 center-mounted、front-mounted、swing-arm 三类；Figure 2 留在这段。再下一段用 mode of control 起头，分成三类：人工随行或乘坐、无线遥操作、规则区域上的自主行走。Kobayashi 的遥操作和 Hwangbo 的固定盘自主行走放在这段。摆臂不放进控制方式。第 15 条仍在 “rigid coupling between disc and body.” 后分段，但后段不再复述几何优势，只留一句过渡：摆臂使抹盘相对基座能动，固定盘上的自主行走因此还不够，然后接第 17 条的 SatAOI。原演进段里盘与基座如何变化，不在控制段里再讲一遍。
处理：按方案改

**11.** 贴在三类构型的第一类旁边：“the disc relative to the base. In the first, the circular disc is mounted under or near the center of the base...”

批注：给三类明确起名 center-mounted，front-mounted，swing-arm；然后每一类都要有参考文献支持。

方案：三类就用这三个名字，Figure 2 的图注和引言里 “beneath or in front of the base” 改成同一组，避免两套说法。每类一句定义加文献，不新找文献。center-mounted：盘在基座下方或近中心，引 hwangbo1999 的乘坐式双转子，以及 shin2003 那台盘在机体下方、靠盘姿态行走的双盘机。front-mounted：引 kobayashi1996，但写明该机在行走机构的前部和后部都装了抹盘，不是只挂在正前方；类名仍用 front-mounted，并用半句说明盘相对基座固定、没有主动侧向运动。swing-arm：盘在主动摆臂末端，只引 lin2025。现有文献里只有这一篇写摆臂构型，不临时补一篇没读过的文献。
处理：按方案改

**12.** 划中整段 “This paper focuses on the third configuration for two reasons. ... cannot be captured by a conventional fixed-width strip model.”

批注：这部分换个思路介绍，不强调我们聚焦第三种；而是突出 swing-arm 机器人具有 xxx、xxx 等优势，得到了越来越多的关注。

方案：删掉 “This paper focuses on the third configuration for two reasons.” 不写本文聚焦第三类。swing-arm 接在三类定义后，用两句写已有优势，不新编优势：摆臂能在基座躲开墙、柱、孔洞和窄口时把抹盘送进这些区域；在扫掠彼此衔接时，同样的基座速度下有效覆盖宽度可以超过盘径。然后一句：这一构型在近期施工机器人研究中受到越来越多的关注，只引 lin2025，不写成已有大量文献。再一句接到规划：这些优势来自基座移动和摆臂摆动的配合，固定宽度条带模型写不出来。紧接着的运动学段删掉重复的侧向覆盖、多余基座行程和湿混凝土转弯，从状态变量写起：\(x_c\)、\(y_c\)、\(\theta\)、\(\phi\) 决定基座、摆臂和抹盘的位姿，基座能过不等于抹盘够得到，抹盘够得到也不等于整机无碰撞。用 disc，不用 base–tool 这套新说法。
处理：按方案改

**13.** 划中 “mobile chassis”。

批注：？？

意图：老师盯上的是 “mobile chassis” 这个词，不是 Kobayashi 这件事实。前文机器人本体一律叫 base，这里突然换成 chassis，读起来像另一个部件。
改法：这句改成 lightweight mobile base，并保持「前后抹盘固定在行走本体上」的事实。不新加文献，也不改成别的机型。
处理：按意图改

**14.** 插在 “perform successive operations from wood floating to steel troweling.” 之后。

插入文字：补充参考文献？

意图：问号是在问这句「从 wood floating 到 steel troweling」有没有出处。出处已经是 Kobayashi et al.，只是 \cite{kobayashi1996} 落在下一句末尾，这句看起来没有文献。
改法：不新找文献。把已有的 \cite{kobayashi1996} 放到 “steel troweling” 这句末尾；下一句若仍在讲同一套系统，可以保留同引。
处理：按意图改

## 第 5 页 · 2.1 末尾到 2.2

**15.** 插在 “coupling between disc and body.” 和 “More recent swing-arm robots...” 之间。

插入文字：建议在这里分段？

意图：这一段把固定盘机器的自主行走和摆臂几何的变化写在一起。问号是建议在话题转换处断开，不是要求重写。
改法：就在 “rigid coupling between disc and body.” 之后分段。前段停在 Hwangbo 的固定盘自主行走，后段从 “More recent swing-arm robots” 起讲几何变化。
处理：按意图改

**16.** 划中整段 “The evolution of troweling robots therefore encompasses both a progression from manual control... introduces a new coordinated base–arm planning problem.”

批注：似乎有些冗余，前面已经提到过机器人构型的事情了。

方案：整句删除，包括 “therefore encompasses both a progression...” 和 “The latter improves flexibility...”。控制方式的演进和盘–基座构型的变化已经在第 10、11 条各说一次，这里不再回收。基座–摆臂协同规划这个缺口也不在这句里预告，交给第 17 条用 SatAOI 停在可作业区域来带出。
处理：按方案改

**17.** 方框圈住 SatAOI 两整段，从 “Among existing systems, the swing-arm platform considered by SatAOI...” 到 “...This is the direct starting point of the present study.”

批注：这两段适当简化。

方案：两段收成一段、四句以内，不重复第 12 条的侧向覆盖和有效宽度。保留的信息是：SatAOI 研究的就是这种摆臂平台；它从障碍栅格出发，建立基座、摆臂和抹盘的模型，搜索机器人能进入且抹盘能作业的连通区域 [lin2025]；输出停在这块可作业区域，没有区域访问顺序，没有基座在区域之间的转移，也没有区域内的基座–摆臂协同覆盖；本文从这块区域出发，规划连续覆盖 route。删掉 “closer to the target” 的铺垫、比固定盘或纯遥操作更完整的评价，以及 “area decomposition, global visitation, local coverage, and speed coordination” 这串重复清单。
处理：按方案改

**18.** 划中四个类名：Idealized coverage methods；Map-enhanced methods；Platform-constrained；Environment–platform coupled methods。

批注：这几个名字的定义和提法要再斟酌一下，map-enhanced、plaform-constrained 等提法要有适当的铺垫或解释？

意图：不是要推翻两轴四分法。这四个名字是本文自己起的，但一出现就像领域里的现成分类，而且 map-enhanced、platform-constrained 没有先解释。plaform 是笔误。
改法：保留这四个名字，不另起一套。第一次出现时先写明它们是本文的称呼，并用各半句对应「地图表示能力 × 机器人行为保真」：理想化（两者都弱）、地图增强（地图复杂、工具足迹固定）、平台约束（运动约束写得细、场景偏规则或局部）、环境–平台耦合（两者都保留）。Table 1 的 Category 列用同一组名字。
处理：按意图改

**19.** 方框圈住整段 “Swing-arm troweling CPP requires both capabilities of the fourth class. ... represented in the same planning model.”

批注：这一段逻辑上毕竟突兀。

意图：「毕竟」按笔误理解成「比较」。这段在四个类还没介绍完时就说摆臂抹平需要第四类，读者还不知道第四类是什么。
改法：整段不删。挪到四类分别介绍完、缺口句 “the two have not yet been unified” 之前，作为收束：因此摆臂抹平需要第四类，地图和基座–摆臂–圆盘行为必须进同一个模型。挪走后，类名定义段不再插这段结论。
处理：按意图改

## 第 6 页 · 2.2

**20.** 贴在 BCD / STC 那句旁边：“BCD partitions an area where scan-line connectivity changes...”

批注：这里要简要介绍一下此类方法的基本原理和思路；后面几类方法类似。

方案：第一、二、三类各补一句基本思路，不写成教程，也不新增算法。第一类：BCD 是扫描线扫过自由空间，线上自由区间的个数变化时结束当前单元，单元内再做往复扫掠；STC 是把自由空间收成粗栅格，在粗栅格上建生成树，再绕树边界走完细栅格。两句的引用仍分别贴在 BCD 和 STC 上。第二类在第 22 条的定义句后补一句：先表示带孔、非凸或有障碍的地图，再用固定宽度条带覆盖，并排列区域、用无碰撞转弯连接。例子仍是 polygon coverage、Fields2Cover、Nobleo。第三类把现有定义收成一句思路：规划时保留最小转弯半径、臂的可达范围和部件碰撞，但场景多是规则场地、局部表面或三维物体。例子仍是 Fields2Cover 的运动学和 Thakar 的喷洒。第四类没有现成方法可介绍，不另起一段；第 19 条挪走的那句继续说明它要同时保留复杂地图和基座–摆臂–圆盘行为。
处理：按方案改

**21.** 划中 “Applied directly to swing-arm troweling, they cannot distinguish the relative poses of the base, arm, and disc or represent how arm-angle changes affect the instantaneous footprint and collision risk.”

批注：换一个表述，这类方法不能考虑 base-disc 的相对位置，arm-angle 等参数变化，因此难以用于 swing-arm……

方案：划中的这句改成老师给的逻辑，不保留 “instantaneous footprint and collision risk” 作为主句。写成：这类方法不表示 base 与 disc 的相对位置，也不表示臂角 \(\phi\) 的变化，因此难以用于 swing-arm 抹平；在这种机器人上，disc 会相对 base 移动。只用 base、disc、arm angle，不另造 footprint 或 collision risk 的说法。碰撞检查仍留在后文模型里，不塞进这句。
处理：按方案改

**22.** 划中 “includes reproducible open-source”。

批注：包括开源资料不是这类方法的本质特质吧？

意图：第二类不该用「开源、可复现」来定义。开源只说明我们为什么能拿它们做对比，类的特征是复杂地图加固定工具足迹。
改法：定义句删掉 “includes reproducible open-source”。第二类改成：能表示复杂地图，但机器人和工具仍主要是固定足迹。开源只在后文点名 polygon coverage、Fields2Cover、Nobleo 时带一句可复现，不写进类定义。
处理：按意图改

**23.** 划中 “frameworks,”。

批注：引用直接对应到具体算法名称上。

方案：第二类现在先写 “frameworks”，引用落在后面的长句上。例子句改为名字当场带引用：polygon\_coverage\_planning 贴 bahnemann2021 和 polygoncoverage，Fields2Cover 贴 mier2023 和 fields2cover，Nobleo 贴 nobleo。后面若只是重复该名字已经引过的事实，不再堆一次引用；Dubins 或 Reeds–Shepp、Spiral-STC 这种新的机制主张，引用留在该机制词上。“These frameworks show...” 收成不带引用的半句。第三类里 Fields2Cover 的最小转弯半径已经贴着 mier2023 和 fields2cover，喷洒消毒已经贴着 thakar2022，这两处不动。不在 “frameworks” 上补一串总引。
处理：按方案改

**24.** 在 “two have not yet been unified for swing-arm floor coverage” 的 “unified” 和 “for” 之间插入 “, especially”。

处理：直接改

**25.** 贴在 “an active arm and circular disc; they are not general judgments of the methods or software.” 旁边。

批注：画一个横纵坐标的图，体现四类算法的关系可能更好？

方案：加一张示意图，不替换 Table 1，也不用实验数据。横轴是 map representation，从规则或简化地图到复杂地图；纵轴是 robot model，从点或固定足迹到带臂角的 base–arm–disc。四个象限用第 18 条的类名。左下是 idealized，放 BCD 和 STC；右下是 map-enhanced，放 polygon CPP、Fields2Cover 和 Nobleo；左上是 platform-constrained，放 mobile manipulator 和 SatAOI；右上是 environment–platform coupled，标成尚未统一，并标上 BiRect。Fields2Cover 和 SatAOI 只放 Table 1 已经指定的那一类，不占两个象限。图放在四个类名定义之后、分类展开之前。图注一句。第 19 条挪走的收束句用半句指向这张图。
处理：按方案改

## 第 7 页 · Table 1 和 2.3

**26.** 贴在 “Table 1: Representative CPP methods and their applicability to swing-arm troweling.” 旁边。

批注：拆分为两列，map representation 和 robot model；tool 还是 robot，建议文中表述统一。

方案：原 “Map and tool model” 拆成 map representation 和 robot model 两列，并与第 27 条一次改完。表头用 robot model，不用 tool model。指固定机具的格子统一写成 fixed footprint；STC 写 point or disc robot；移动机械臂写 mobile manipulator；SatAOI 写 base, arm, and disc；本文这一行的方法名改成 BiRect，robot model 写 swing arm with a time-varying disc。其他论文的机具在优缺点里仍可称 tool 或 end-tool。地图列保持现在的说法：cellular decomposition、grid spanning tree、polygon with holes、non-convex field、occupancy grid、three-dimensional surface、construction obstacle map、two-dimensional obstacle map。不改各方法被分到哪一类。
处理：按方案改

**27.** 划中表头 “Map and tool model”。

批注：最后一列改为 pros & cons，然后分条列举，前面用 √ 或 x 区分优劣势。

方案：最后一列 “Relevance to swing-arm troweling” 改为 Pros and cons。每行两条，前面用 \(\checkmark\) 和 \(\times\)，文字从现有格子里拆出，不新加实验结论。BCD：能在单元内组织往复扫掠；不能表示主动摆臂和连续扫掠。STC：能系统遍历栅格；不能利用臂运动带来的时变盘位。Polygon CPP：能给出备选条带和避障转移；不能表示臂的瞬时盘位。Fields2Cover：含条带、路线顺序和曲率受限连接；固定足迹不含摆臂。Nobleo：能把栅格覆盖接进导航；不能协调臂角、臂角速度和基座速度。移动机械臂：能同时规划基座停放和末端运动；不能走完复杂二维地面。SatAOI：能确定可作业区域及其连通；不能给出访问顺序或连续覆盖 trajectory。BiRect：把矩形分解、访问、局部摆扫和轨迹评价接在一起；目前假设静态地图，并用启发式搜索。表仍用 longtable，这一列每行两短行。
处理：按方案改

**28.** 划中 “[8, 14, 15, 16, 17, 18, 19, 20, 21]”。

批注：拆分引文。

方案：这串挂在 2.3 开头段末，是 lin2025、choset1998、gabriely2001、bahnemann2021、polygoncoverage、mier2023、fields2cover、nobleo、thakar2022，对应 PDF 的 [8]、[14]–[21]。按半句拆开，不新增文献。BCD 贴 choset1998，STC 贴 gabriely2001；带孔或非凸区域上的分解与条带贴 bahnemann2021 和 polygoncoverage；栅格遍历贴 nobleo；Fields2Cover 的转弯和曲率受限连接贴 mier2023 和 fields2cover；移动机械臂的可达与碰撞贴 thakar2022；SatAOI 确定可作业区域贴 lin2025。段末不再留总引。各篇结论不改。
处理：按方案改

## 第 8 页 · 2.3 Research Gap

**29.** 贴在 “First, existing CPP methods do not model active arm behavior...” 这三段旁边。

批注：这里的三段话建议适当简化，要简洁，毕竟细节前面都讨论过了，这里不宜反复。

方案：三条缺口各留一个主题句，加上已经定下的改写，不再把 2.2 的方法清单重讲一遍。第一条：主题句里用半句说明常规 CPP 的机具固定在 base 上，定了 base 的 route 就定了覆盖；接着只接第 30 条的两句。第 31 条删掉的 SatAOI 句不恢复。第二条：主题句接第 33 条留下的一句。第 32 条那串引用不留在这里。第三条：主题句、最大臂展只说明某些位姿下 disc 够得到、再接第 35 条并成的一句。第 36 条删掉的两段不恢复。三条都用 base、disc 和 arm angle，不用 end disc、end tool 或 body。
处理：按方案改

**30.** 划中整段 “For a swing-arm robot, the same base position and heading admit multiple arm poses... during execution.”

批注：没看明白？

意图：老师卡在第一条研究缺口里的这几句，不是要求删掉。同一基座位姿可以有多个臂角、最大臂展不等于连续覆盖、整机碰撞要同时看，三件事叠在一起，没有一个具体情形。
改法：这段保留，改成两句。先写同一基座位置和航向，臂角不同则盘心在半径为臂长的弧上，整机碰撞状态也不同。再写最大臂展或加宽条带只说明某个位姿够得到，不等于连续运动中覆盖到。用词与后文的臂角 $\phi$、盘心位置一致，不另造说法。
处理：按意图改

**31.** 删去，没有文字说明：“SatAOI models the geometry and collision relationships among these components but uses them primarily to determine workable positions rather than continuous coverage motion [8]. The present method therefore preserves the relationship among base motion, arm rotation, and the circular-disc sweep during both trajectory generation and evaluation.”

处理：直接改

**32.** 划中 “[16, 17, 18, 19, 20]”。

批注：拆分引用。

方案：这串是第二缺口里 “polygons with holes ... fixed tool footprint” 句末的 [16]–[20]，即 bahnemann2021、polygoncoverage、mier2023、fields2cover、nobleo。第 29 条把第二缺口收成主题句加第 33 条那一句后，这句复述不再保留，句末总引也不再出现。对应关系留在 2.2 和第 28 条：多边形分解贴 bahnemann2021 和 polygoncoverage，Fields2Cover 贴 mier2023 和 fields2cover，占据栅格贴 nobleo。第 33 条留下的那句不引这五篇。
处理：按方案改

**33.** 划掉整段 “SatAOI identifies workable regions and their connectivity but does not proceed to visitation ordering... controlling the candidate-search space.”

批注：都可以不要或简单提一句。

意图：第二条 gap 大段复述了前面的综述。老师给了两个选择：整段删，或只留一句。默认取信息量更大的那一个，避免第二条 gap 消失。
改法：不整段删除。留一句：SatAOI 停在可作业区域；本文用分层启发式把区域连通、访问顺序和区域内的基座–摆臂覆盖接成一条可计算的链路。BCD、Fields2Cover 和机械臂覆盖不再在这句里复述。
处理：按意图改

**34.** 划中 “a static reachability envelope”。

批注：这个概念之前是否提过？

意图：static reachability envelope 在引言里出现过一次，但没有定义，到 2.3 又当作已知术语。老师问的是「读者能不能知道它是什么」，不是要删第三条 gap。
改法：保留这个概念。引言第一次出现时定义成一句话：静态可达包络是臂在若干位姿下能碰到的区域，不含基座行进和摆臂的时间过程。2.3 再用时直接指回这句，不重新起名。
处理：按意图改

**35.** 贴在 “continuous base advance and periodic arm swinging, coverage continuity depends on the number of sweeps per unit distance...” 旁边。

批注：简化。

方案：划中的这句和后面 “If the base is too fast or the arm too slow...” 并成一句：base 持续前进、swing arm 周期摆动时，相邻两次扫掠的纵向间距由基座速度和臂角速度决定；基座太快或摆臂太慢就会留下未覆盖间隙，即使目标落在静态可达包络里，够得到也不等于覆盖到。删掉没有定义的 “number of sweeps per unit distance”，也不在这里引入新符号。静态可达包络按第 34 条用引言里的定义。第 36 条删掉的两段不在这里补回。
处理：按方案改

**36.** 划掉两段。第一段：“This paper incorporates the relationship between base and arm velocities into the coverage analysis...” 第二段从 “In summary, the core research gap is...” 到 “...under the specified velocity relationship.”

批注：可删去。

处理：直接改

## 第 9 页 · 3.1 Overall Planning Pipeline

**37.** 删去 “data flow.”，改为 “workflow”。

处理：直接改

**38.** 贴在 Figure 3 说明 “Coverage-planning framework and principal data flow...” 旁边。

批注：global routing 还是 global route planning？建议前后统一。

意图：老师看到图或图注里的 global routing 和后文小节名 Global Route Planning 不是同一个说法，要求选定一个。正文小节名已经是 Global Route Planning。
改法：统一用 global route planning，包括图内标签。不再使用 global routing。若图里印着 routing，改图中的文字，不改模块结构。
处理：按意图改

**39.** 划掉 Figure 3 标题后半整段，从 “The inputs on the left are the work map...” 到 “...and planning time.”

批注：图片标题要简化，后面所有图表都类似处理。

方案：图注只写这张图是什么。正文或图内已经有的输入、符号、颜色、数值和结论不进图注。Figure 3 收到一句：“Workflow of BiRect.” 用第 37 条的 workflow，不用 data flow，也不用 framework；不在图注里列 \(\mathcal R_1\)、\(G\)、\(\Pi\)、\(q(t)\)、覆盖率和 \(T_{\mathrm{plan}}\)。后面的长图注按同一规则删去第二句及以后：矩形覆盖原语、与 Fields2Cover 的覆盖对比、扫描策略、速度比。面板编号若是看图所必需，留在第一句里。第 50、52 条已经规定删法的图注仍按那两条，不改回长注。表题保持一句，不套用这条。
处理：按方案改

**40.** 贴在 “The rectangular-decomposition module first generates candidate rectangles...” 旁边。

批注：前面补充：to improve the efficiency of ...

意图：省略号空着的是「提高什么的效率」。结合后文对候选搜索规模的讨论，这里指的是规划搜索的计算效率，不是抹面作业效率。
改法：矩形分解那句前补目的：to improve the efficiency of searching a complex free space。意思是把自由区域收成少量候选矩形，而不是在整张图上直接搜索轨迹。不写成提高抹面效率。
处理：按意图改

**41.** 贴在 “For every rectangle, the local-modeling module constructs two primitive types...” 旁边。

批注：是否有必要分段？

意图：问的是 3.1 里「每个模块单独起一段」是否把一条流程切碎了。倾向是不必在局部运动这里再断段。
改法：矩形分解和连通补全仍可分段，因为输出不同。局部运动这段并回前面的流程，用 Then 接上，不单独起段。3.1 保持「四个阶段一条叙述」。
处理：按意图改

**42.** 划中 “enter”。

批注：表述是否合适？

意图：老师问的是 “enter the global route search”。costs enter a search 这个动词含糊，读不出这些时间是搜索用的代价。
改法：enter 改为 are used as the costs of。整句意思是：覆盖、通行和边上的转移时间一起作为全局路径搜索的代价。模型不改。
处理：按意图改

**43.** 贴在 “conservative-grid generation through trajectory evaluation is T_plan...” 旁边。

批注：3.1 的核心是讲清楚算法的总体大逻辑，以及各个模块的关系，建议进一步思考和优化相关表述。

方案：3.1 改成按数据交接来写，模块内部规则留给后文。开头一句：BiRect 分四段，上一段的输出是下一段的输入。然后四句。矩形分解把复杂自由空间收成少量双向矩形候选，目的用第 40 条的搜索效率。连通补全输出可行邻接图 \(G\)，边表示存在满足几何和速度约束的基座–摆臂转移，不只是矩形相接。局部运动按第 41 条用 Then 接上：每个矩形给出首次覆盖和再次通行的时间，这些时间按第 42 条作为 global route planning 的代价。全局段在 \(G\) 上得到访问序列并连成 trajectory；评价只读这条 trajectory，得到覆盖率和执行时间，\(T_{\mathrm{plan}}\) 是整段流程的计算时间，不作为搜索代价。\(\mathcal R_1\)、\(T_{\mathrm{cover}}\)、\(T_{\mathrm{transit}}\) 和 \(\rho\) 的定义不在 3.1 先写一遍。用 workflow 和 global route planning，不新增模块名。
处理：按方案改

## 第 10 页 · 3.2.1 从场景到规划输入

**44.** 只高亮、没有写字，五处：

- “extracted from a CAD/BIM model, site-survey data, or localization”
- “Walls, columns, equipment foundations, embedded components, reserved openings, and areas outside the work boundary are marked as unavailable.”
- “from CAD/BIM, field measurement, and mapping”
- “into spatial cells at a common resolution.”
- “black pixels represent walls, columns, openings, out-of-bound areas, and areas excluded by the safety margin.”

意图：这五处没有写字，和下面四支箭头是同一件事：3.2.1 把「场景里哪些区域不可用、再变成黑白像素」说了三遍。高亮标的是重复出现的短语。
改法：不把五处高亮当成五条独立修改，与 45、46、47 一起改。3.2.1 只留一条从场景到二值图的叙述。第二段删掉与第一段重复的 CAD/BIM、不可用区域和黑白像素定义，只保留第一段没有的三件事：分辨率 $s_p$、蓝色是结果叠加而不是第三种输入、刚体变换 $T_{WM}$。第三段若只是把第一段再说细，压成两三句保守规则（边界或含糊的单元判为不可用，曲线变成阶梯边界）。「格内必须全是自由像素」的公式留给 3.3，这里不提前展开。
处理：按意图改

**45.** 页左边有四支箭头，没有写字，分别挨着这四段：

- “are marked as unavailable. The remaining floor... becomes the target work region. ... dilated by a margin before rasterization.”
- “then rasterized and geometrically calibrated to produce a physically scaled binary work map, which is the direct map input to CPP.”
- “Blue is an overlay... A rigid transform [calibrates] image coordinates to world coordinates...” 一直到 “The conversion from planar geometry to the binary map follows uniform labeling”
- “same plane and classified at one resolution... Cells on an obstacle boundary or with ambiguous membership are treated as unavailable...”

意图：四支箭头没有写字，分别指着 3.2.1 里前后重复的四段，和 44 的高亮是同一处意见。
改法：与 44、46、47 一起改，不单独为每支箭头加句子。压缩方式见 44。
处理：按意图改

**46.** 贴在 “unavailable-region contours can be dilated by a margin before rasterization...” 旁边。

批注：前后表达不一致，且有重复。

意图：第一段说不可用区域可以先膨胀再栅格化，后面又用安全边距把边界单元判成不可用，两套说法并列，读者会以为是两件不同的事。
改法：与 44、45、47 一起改。膨胀边距 $\delta_{\mathrm{map}}$ 和「边界单元判为不可用」合成一条保守规则：先按安全边距扩大不可用区域，再栅格化，边界上的单元一律算不可用。不保留两套互相独立的措辞。
处理：按意图改

**47.** 贴在 “The conversion from planar geometry to the binary map follows uniform labeling and conservative discretization...” 旁边。

批注：下面的内容其实是上面表述的细化，会让人觉得繁冗且不清晰。

意图：第三段 “uniform labeling and conservative discretization” 是在把上面两段再讲一遍，不是新步骤。
改法：与 44–46 一起改。第三段不再复述分类和黑白定义，只留保守栅格化的操作规则，公式放在 3.3。
处理：按意图改

## 第 11 页 · Figure 4 和 3.2.2

**48.** 贴在 “Figure 4: Conversion from exact geometric descriptions...” 旁边。

批注：小标题放到图片下方。

意图：「小标题」指图内 (a)(b)(c) 各子图的标题，不是已经位于图下方的 Figure 图注。现在这些子图标题在图块上方。
改法：Figure 4 各子图标题移到对应子图下方。LaTeX 总图注仍留在整幅图下方，不重复搬一次。
处理：按意图改

**49.** 红圈画在 Figure 4 子图 (d) “L-Shaped Region with Multiple Obstacles” 右侧栅格图里，白色区域右下角的一小团黑色栅格上，箭头从便签指过去。

批注：这个地方对吗？

意图：红圈在 Figure 4(d) 右侧栅格、白色区域右下角的一小团黑格上。老师怀疑这团黑格对不上左侧精确几何里的障碍，像栅格化画错了。
改法：先核对这团黑格是不是左侧某个障碍或保守膨胀的结果。对不上就改图，使黑格与左侧障碍一致；对得上就不动几何，图注用半句说明它是该障碍的栅格结果。不用图注掩盖对不上的格子。
处理：按意图改

**50.** 划掉 Figure 4 标题后的整段说明，从 “The left column shows exact two-dimensional work regions...” 到 “...irregular areas with dense obstacles.” 没有另外写字。

处理：直接改

**51.** 划中公式里的 “255”（“Let the input map be M ∈ {0, 255}^{H×W}”）。

批注：直接强制限定 255 是否合适？是否应该根据最大可允许的 cell_size 反算？

意图：老师把像素标签 255 和物理格子尺寸 cell size 看成了同一件事。255 只是 8 位图像里「白、自由」的约定标签，不是长度，不能由 $s_p$ 或规划格大小反算。
改法：不改实验图像的编码，也不用 cell size 反算 255。公式可以保留 $M\in\{0,255\}$，紧跟一句：0 和 255 只区分障碍和自由，不是灰度，也不是物理量。像素尺寸 $s_p$ 和规划格大小仍在各自的定义里给出。
处理：按意图改

## 第 12 页 · Figure 5

**52.** 划掉 Figure 5 说明里的这句，没有另外写字：“The diagram identifies the base center, θ, φ, r_d, L, d_p, ... and base length and width. These quantities determine the robot’s occupied geometry and the disc-center position in Eq. (1).”

处理：直接改

## 第 13 页 · 3.2.2 末尾到 3.3

**53.** 划中 “work quality,”。

批注：这个不好度量吧？

意图：这里的 work quality 实际是覆盖率 $\rho_{\mathrm{work}}$，不是抹面平整度。引言里 work quality 又指表面质量，同一个词变成了无法从轨迹里测出来的指标。
改法：目标函数处的 work quality 改成 effective-work coverage，仍指 $\rho_{\mathrm{work}}$，定义不变。引言里表示抹面观感的 work quality 改成 surface finish，避免一个词指两件事。
处理：按意图改

**54.** 只高亮 “task-level quality”，没有写字。

意图：没有写字，是第 53 条对 “quality” 的同一疑问，用在 “task-level quality measure $\rho_{\mathrm{work}}$” 上。
改法：与 53 一起改。task-level quality measure 改成 task-level coverage measure，仍指 $\rho_{\mathrm{work}}$。不另写一段解释。
处理：按意图改

**55.** 只高亮 “global visitation candidates;”，没有写字。所在句是 “objective supplies time costs to local primitives and global visitation candidates”。

意图：这句把事后的全程时间 $T_{\mathrm{exec}}$ 写成了搜索里供给「全局访问候选」的代价。搜索实际用的是局部覆盖、通行和转移的时间代理，不是 $T_{\mathrm{exec}}$ 本身。老师划出这句话，是因为候选和代价的关系读不通。
改法：改成：搜索使用局部覆盖、通行和转移的时间代理来比较访问序列；全程执行时间 $T_{\mathrm{exec}}$ 在轨迹生成之后计算，不在搜索里当代价。删掉 “supplies time costs to global visitation candidates”。
处理：按意图改

**56.** 划中小节标题 “Conservative Rasterization”。

批注：这个是不是前面讲过了？

意图：3.2.1 已经讲了保守栅格化，3.3 的标题又从头讲一遍。老师要去掉重复，不是要删掉规划格上的公式。
改法：3.3 开头不重讲为什么要保守。用一句「沿用 3.2.1 的保守规则，这里写成规划格上的判定」接上公式 (5)。「格内像素必须全是自由」只留在 3.3。3.2.1 的压缩见 44–47。
处理：按意图改

**57.** 在 “with all planning cells inside R_free” 句末、紧挨 R_free 后面插入 “are”。下一句是 “Candidates whose width or height is below a specified minimum are removed.”

意图：老师看到 “with all planning cells inside R free” 语法不完整，想补上 are，让它变成「矩形里的规划格都是自由的」。插在 $R$ 后面会变成 “R are”，句子仍然不通。
改法：不在 $R$ 后硬插 are。矩形定义之后单独写一句：All planning cells inside $R$ are free. 下一句 “Candidates whose width or height...” 不动。
处理：按意图改

**58.** 划中 “Cardinalities”。

批注：什么意思？

意图：Cardinalities 是集合元素个数的数学术语，指 $|\mathcal U(R)\setminus\mathcal A|$ 这类绝对值是规划格的个数。老师是读不懂这个词，不是在问公式对不对。
改法：删掉 Cardinalities。改成：式中的绝对值表示规划格个数，所以 $\alpha$ 的单位是格，$\beta$ 无量纲。公式 (7) 不改。
处理：按意图改

## 第 14 页 · 3.3

**59.** 划中 “Final Segmentation”。

批注：？？什么含义？前面或 3.1 是否有铺垫。

意图：Connectivity Completion and Final Segmentation 里的 final segmentation 没有定义，也容易和前面的矩形分解混在一起。这一节实际做的是连通补全，输出最终矩形集和可行图。
改法：小节标题改为 Connectivity Completion。第一次写出最终矩形集 $\mathcal R$ 时说明它是补上桥接矩形之后的集合。不再使用 final segmentation。3.1 里可以继续说 final rectangle set，但不说 segmentation。
处理：按意图改

## 第 15 页 · Figure 6

**60.** 贴在 “Figure 6: Single-rectangle coverage primitive...” 旁边。

批注：这幅图太大了，其实应该适当缩小；另外，是不是针对不同长宽比的矩形，都给出相应的路径策略？

意图：前半句是版式。后半句是在问路径是否随矩形长宽比改变；如果变，图就应该画出不同比例，如果不变，现在这一张容易让人以为只适用于一种矩形。
改法：图缩小到约半栏宽。不按长宽比新画多张图。局部路径都是沿矩形一条轴的往复条带：默认用长边以减少换道，另一条轴也生成一遍再比时间。图旁加一句说明这一点。
处理：按意图改

**61.** 划掉 Figure 6 标题后半句，没有另外写字：“The disc entry and exit are determined by neighboring rectangles or the initial state. The local planner compares time proxies for both sweep directions and feasible starting corners, then covers the rectangle through forward base motion and reciprocal arm swinging.”

处理：直接改

## 第 16 页 · Algorithm 1

**62.** 贴在页面顶部 “Algorithm 1 Rectangle segmentation and connectivity completion” 旁边。这个算法在 3.4 末尾被引用，浮动到了第 16 页，已经跨过 3.5 的开头。

批注：要跟对应小节放到一起，不要跨小节。

处理：直接改

## 第 17 页 · 3.5.2

**63.** 贴在 3.5.2 标题上方。

批注：3.5 节内容要有适当的原理图或示意图辅助解释。

方案：3.5 已有 Figure 6 画矩形内的往复路径，第 60 条把它缩小，并说明默认沿长边、另一条轴也比一次。这里再补两张原理图，不按长宽比重画整条路径。第一张放在 3.5.2 开头，三幅小图。(a) 入口：disc 的圆心在矩形边界上，base 沿航向退到边界外，间距是 \(d_p+L\)。(b) 条带：沿条带的长度是 \(\ell_R\)，横向总宽是 \(h_R\)，每条 work strip 宽 \(w_s\)，条数 \(N_s\)，标出一个起始角。(c) 振幅：臂角相对中位为 \(\pm\phi_w\)，横向覆盖标成 \(w_s\)，并标出臂长 \(L\) 和盘半径 \(r_d\)。\(\phi_w\) 和 work strip 的文字定义仍按第 64、65 条，图只标这些已有符号。第二张放在 3.5.3：base 在臂从 \(-\phi_w\) 摆到 \(+\phi_w\) 的时间里前进一个盘直径，相邻半周扫掠因此相接，标出 \(v_{\mathrm{work}}\) 和 \(T_{\mathrm{half}}\)。3.5.4 的四项时间不另作图，仍按第 66 条用文字和式 (18) 对齐。图注各一句。
处理：按方案改

**64.** 划中标题中的 “Swing Amplitude”。

批注：什么意思？前面是否有解释或定义？

意图：Swing Amplitude 出现在 3.5.2 的标题里，但前文只说过摆臂，没有定义振幅。后文的 $\phi_w$ 才是它：覆盖一条条带所需的臂角半幅。
改法：3.5.2 开头先定义：swing amplitude 是覆盖一条条带时，臂角相对中位来回摆动的半幅，记为 $\phi_w$，由条带宽度、盘半径和臂长决定。标题保留。公式不改。
处理：按意图改

**65.** 只高亮 “work strips.”，没有写字。

意图：没有写字，和前一条一样，是这个词还没定义就拿来用。work strip 指矩形内沿一条方向往复覆盖的一条作业带。
改法：在 $\ell_R$、$h_R$ 的定义前加半句：work strip 是圆盘沿矩形一条边往复覆盖时的一条作业带。$\ell_R$ 是一条作业带的行驶长度，$h_R$ 是各条带一起跨过的横向宽度。定义本身不改。
处理：按意图改

## 第 18 页 · 3.5.4

**66.** 划中 “The first visit to a rectangle includes motion to the starting corner, coverage of all strips, lane changes, turns, arm deployment and retraction, and departure from the rectangle.”

批注：没太看懂。

意图：老师对不上「第一次访问包含哪些动作」和后面时间公式的四项，尤其 “departure from the rectangle” 可能和矩形之间的交接时间算了两次。
改法：公式 (18) 不改。文字改成与四项对齐：条带行驶、换道、原地转角、摆臂调整。写明矩形之间的交接时间在边代价 $c_{ij}$ 里，不进入 $T_{\mathrm{cover}}$；驶向本矩形出口若发生，算在换道或转角里。
处理：按意图改

## 第 20 页 · 3.7

**67.** 贴在 “3.7 Work Coverage and Full-Trajectory Coverage” 标题上方。

批注：建议补充原理示意图。

方案：在 3.7 区分有效作业段和非作业段之后、两个覆盖率公式之前，加一张原理图，不用实验地图。画两个相邻矩形和一次转移。(a) 作业条带上的摆扫标成有效作业；换道、原地转向、臂的展开或收回、矩形之间的交接标成非作业。(b) 同一条 trajectory 上涂两层：只由作业段 disc 扫过的区域是 \(\mathcal C_{\mathrm{work}}\)，再加上非作业段 disc 扫过的区域是 \(\mathcal C_{\mathrm{traj}}\)。分母仍是自由像素集合，不在图里重写公式，也不新增第三种覆盖率。图注一句：work coverage 只计作业条带上的圆盘扫掠，full-trajectory coverage 把转移和调整时的扫掠也计进去。
处理：按方案改

## 第 21 页 · 4 Experiments

**68.** 在 “Three groups of experiments evaluate the proposed swing-arm CPP method.” 的 “experiments” 和 “evaluate” 之间插入 “are designed to”。改完是 “Three groups of experiments are designed to evaluate...”。

处理：直接改

**69.** 划中 “clarify the difference”。

批注：不是澄清差异，而是突出或验证我们算法的有效性和优势。

方案：第一组实验的目的改成验证 BiRect 的优势：在障碍地图里，主动摆臂给出可执行覆盖，全程覆盖率高于固定宽度条带。删掉 “clarify the difference”。不把更短的时间写成待验证的优势，因为表里 Fields2Cover 的时间更短，但路径检查没有通过。第 68 条的 “are designed to” 保留。第二、三组仍分别验证双向候选和 base–arm velocity coupling，不改成同一句套话。
处理：按方案改

**70.** 划中 “map_test1”，另外只高亮了 “parkingGraph”，没有单独写字。

批注：地图名字可以简化，比如 simple，complex 或者干脆编号即可，没必要叫 map_test1。

意图：老师给出了两套可选名字，没有指定用哪套。图里 map_test1 已经标成 map_simple，正文仍写 map_test1，parkingGraph 两处都不统一。
改法：采用 simple / complex，不另编 1、2、3。正文和图中的 map_test1 改为 simple，parkingGraph 改为 complex。三张方向图仍用 scan_comb_corridors、scan_mixed_weave、scan_offset_rooms。实验数据文件名可以不改，正文不再出现 map_test1 和 parkingGraph。
处理：按意图改

**71.** 划中 “in which white pixels are free target area and black pixels are obstacles or unavailable regions.”

批注：不必重复，就说按照前面的定义即可。

处理：直接改

**72.** 贴在 “velocity 90°/s. The minimum rectangle side length is 2.5 m, the greedy-selection weights are α = 0.5 and β = 2.0, and the random seed is 42.” 旁边。

批注：这里建议补充 speed 参数的组合。

方案：公共参数段补上实际一起使用的速度，不新跑实验，也不再只并列三个上限。除速度实验外，三台上限同时使用：基座线速度 \(2.00\) m/s，基座角速度 \(30^\circ\)/s，臂角速度 \(90^\circ\)/s。实际作业速度仍由 3.5.3 的 \(v_{\mathrm{work}}=\min(v_{\max},v_{\mathrm{safe}})\) 决定，上限不写成每条条带的行驶速度。速度实验保持臂角速度 \(90^\circ\)/s 和基座角速度 \(30^\circ\)/s，基座线速度取 \(0.5\)、\(1.0\)、\(1.5\)、\(2.0\)、\(2.5\)、\(3.0\) m/s 六档。Fields2Cover 的条带 \(2.0\) m/s、转弯和连接 \(0.5\) m/s 仍留在 4.1 的对照设置里，不写进这组机器人速度。不增加臂角速度的另一组扫描。
处理：按方案改

**73.** 划中小标题 “Comparison with Fields2Cover”。

批注：小标题优化和调整。

方案：4.1 的小标题由 “Comparison with Fields2Cover” 改为 “Executability and Coverage against Fields2Cover”。标题点出这一节要验证的两件事：路径能否执行，以及全程覆盖率。Fields2Cover 仍留在标题里，标明对照对象。不改成软件综述式标题。
处理：按方案改

**74.** 贴在 Fields2Cover 介绍段旁边：“class of problem. It is supported by a peer-reviewed publication and continuing open-source development...”

批注：fields2cover 算法的介绍建议放到 review 部分，这里不必重复。

方案：实验节删掉 Fields2Cover 的功能清单和开源评价，包括期刊论文、持续开源、多种算法、headland、条带生成、路线顺序和曲率受限连接。这些内容 2.2 已经有，不把本段再搬回去扩写。4.1 只留一句：Fields2Cover 是 2.2 里的固定宽度代表，用来验证第 69 条的可执行覆盖和覆盖率。紧接着保留对照设置：作业宽度 \(1.50\) m、自由区域腐蚀 \(0.45\) m、全程轨迹评价，以及条带 \(2.0\) m/s、转弯和连接 \(0.5\) m/s。
处理：按方案改

**75.** 贴在表中 “map_test1 Proposed 611.00 575.00 94.11 ... Fields2Cover ...” 那一行旁边。

批注：加粗我们的算法名称及其占优势的指标。

方案：表中方法名改为 BiRect 并加粗。只加粗 BiRect 占优的格子：两张地图的全程覆盖率 \(94.11\%\) 和 \(95.73\%\)，以及路径检查的 Passed。不加粗评价面积和覆盖面积，因为两行的评价区域不同。不加粗执行时间和规划时间，Fields2Cover 更短，但论文已说明那是未通过路径检查的生成结果。Fields2Cover 一行不加粗。
处理：按方案改

## 第 22 页 · 4.2 扫描策略表

**76.** 便签贴在表里 “row-then-col” 被换行拆开的 “col” 旁边。这张表是各扫描策略的 coverage / overlap / time。

批注：加粗占优势的 strategy 及其测评数据。

方案：按列加粗，不把整行 row-then-col 都加粗。覆盖率越高越好，overlap 越低越好，时间越短越好；该列唯一最好或并列最好的策略名和数字加粗。Final partition coverage 全是 \(100\%\)，不加粗。三档完全相同的列不加粗，所以 parkingGraph 的 greedy coverage 和 overlap 不加粗。按这个规则：simple 上，row-then-col 的 greedy coverage、overlap 和全程覆盖率加粗，时间加粗的是 row-only 与 col-only 的 \(696.89\) s。complex 上，全程覆盖率加粗 col-only 的 \(95.90\%\)，时间加粗 row-only 和 row-then-col 的 \(5844.73\) s。三张方向图和五行平均里，占优的都是 row-then-col 的 greedy coverage、overlap、全程覆盖率和时间。策略名用 `\mbox{row-then-col}`，避免 col 被拆到下一行。地图名按第 70 条用 simple 和 complex。数字不改。
处理：按方案改

## 第 23 页 · 4.2 末尾到 4.3

**77.** 划中 “row-then-column averages 94.32% coverage,”。

批注：表述比较奇怪？

意图：“row-then-column averages 94.32% coverage” 奇怪在两处：没说是哪一种覆盖率，而且把策略写成了会求平均的主语。摘要里同一个数字是五张图的平均全程覆盖率。
改法：改成：五张图上，row-then-column 的平均全程覆盖率是 94.32%，row-only 和 column-only 分别是 93.96% 和 93.98%。点明是 full-trajectory coverage 的算术平均。数字不改。
处理：按意图改

**78.** 划中 “Effect of Base–Arm Velocity Coupling”。

批注：表述前后统一。

意图：划的是小节标题 Effect of Base–Arm Velocity Coupling。正文里同一件事还叫 velocity matching、velocity relationship、coupled velocities，数量又叫 velocity ratio $\rho$。老师要的是一个名字，没有指定留哪一个。
改法：这件事统一叫 base–arm velocity coupling。$\rho=v/\omega_a$ 只作为这个耦合的比值，不把 ratio、matching、relationship 再当作并列的概念名。小节标题保留。第一次出现时用一句话定义：耦合指基座线速度和臂角速度的配合。
处理：按意图改

## 第 24 页 · Figure 7

**79.** 贴在 “Figure 7: Coverage paths and swept regions for the proposed method and Fields2Cover...” 旁边。

批注：图片放到前面实验介绍部分，方便图文对照。

处理：直接改

## 第 25 页 · 4.4 Discussion

**80.** 划中 “the contribution is not simply another decomposition,”。所在句是 “The three experiments support one central conclusion: the contribution is not simply another decomposition, but the use of coordinated base motion and end-disc swinging...”

批注：什么意思？

意图：老师读不懂 “the contribution is not simply another decomposition”。这句是在反驳一个论文里没有出现的说法，读者不知道「另一种分解」指什么。
改法：删掉 “not simply another decomposition” 这种反驳句。讨论的结论改成正面三句，对应三个实验：相对固定宽度条带，摆臂能在障碍图里给出可执行覆盖；双向候选减轻单一扫描方向留下的区域；基座速度相对摆臂角速度决定覆盖和工时。不新加贡献点。
处理：按意图改

## 第 26 页 · 覆盖率曲线

**81.** 贴在 “(a) map_test1 (b) parkingGraph” 这张图旁边。

批注：这里感觉没有把核心结论或亮眼的结论展示出来？1. full coverage 指标是不是合适？或者换一个单纯某个矩形 strip 的 coverage？2. 横轴从 0 开始可能更好？3. 这个过程是不是还跟 disc radius 或 arm length 有关系？

意图：全程覆盖率从大约 96% 降到 85%，曲线太平，结论不显眼。老师怀疑该看单条作业带的覆盖，并提醒横轴不是从 0 起，而且盘半径和臂长在实验里是固定的，图却像一般结论。
改法：不新跑盘径或臂长实验。现有表只有全程覆盖率，没有单条带覆盖率，所以不另画一条没有数据的曲线。横轴 $\rho$ 从 0 画起。图注写明 $r_d=0.75$ m、$L=1.20$ m、臂角速度 $90^\circ$/s 固定，结果不外推到其他盘径和臂长。正文说明全程覆盖率包含换道和转移，所以降幅比单条作业带温和。结论句改成：基座相对摆臂越快，相邻扫掠的间隙越大，全程覆盖率下降，工时也下降。
处理：按意图改
