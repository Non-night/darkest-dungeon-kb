# Buff duration_type 索引

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


> 只使用下列 12 个已知合法值；非法参数的引擎结果当前未确认。

- [round](round.md)：小回合；每次正常个人回合结束后，持续时间减 1。
- [combat_end](combat_end.md)：每场战斗结束时，持续时间减 1。
- [quest_end](quest_end.md)：每次任务（副本）结束时，持续时间减 1。
- [quest_complete](quest_complete.md)：任务（副本）完成时，持续时间减 1。
- [quest_not_complete](quest_not_complete.md)：任务（副本）未完成并结束时，持续时间减 1。
- [activity_end](activity_end.md)：英雄的城镇活动结束时，持续时间减 1。
- [idle_start_town_visit](idle_start_town_visit.md)：英雄在城镇闲置并发生过周时，持续时间减 1。
- [till_removed](till_removed.md)：持续到被其他规则移除。
- [none](none.md)：无持续时间类型。
- [before_turn](before_turn.md)：个人回合开始前，持续时间减 1。
- [after_turn](after_turn.md)：个人回合结束后，持续时间减 1。
- [after_round](after_round.md)：战斗整轮结束后，持续时间减 1。
