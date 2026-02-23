from pydantic import BaseModel, Field


class ServerDefaultSettingsDTO(BaseModel):
    datepicker: str
    default_cert: str = Field(alias="defaultCert")
    default_key: str = Field(alias="defaultKey")
    expire_diff: int = Field(alias="expireDiff")
    ip_limit_enable: bool = Field(alias="ipLimitEnable")
    page_size: int = Field(alias="pageSize")
    remark_model: str = Field(alias="remarkModel")
    sub_enable: bool = Field(alias="subEnable")
    sub_json_enable: bool = Field(alias="subJsonEnable")
    sub_json_uri: str = Field(alias="subJsonURI")
    sub_title: str = Field(alias="subTitle")
    sub_uri: str = Field(alias="subURI")
    tg_bot_enable: bool = Field(alias="tgBotEnable")
    traffic_diff: int = Field(alias="trafficDiff")

    model_config = {
        "populate_by_name": True
    }
