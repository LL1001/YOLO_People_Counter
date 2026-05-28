"""告警管理模块。"""


class AlertManager:
    """人数告警管理占位类。"""

    def __init__(self) -> None:
        """初始化告警管理器。"""
        self.enabled = False

    def check_alert(self, people_count: int) -> bool:
        """检查是否触发告警占位方法。"""
        # Phase 1 暂不实现告警规则。
        _ = people_count
        return False
