from dtk_api import DtkStdApi
from dtk_api.gen import GoodsListSuperGoodsArgs
from fastapi import Depends, Body
from structlog.stdlib import BoundLogger

from core.logger import get_logger
from core.resp.base import ApiResp
from core.resp.tbk import GenericItemListResponseModel
from core.shared import AppErrno
from core.vendor.dtk import get_dtk_std
from ...api.app import app
from ...api_utils import api_inner_wrapper


@app.post(
    "/dtk/super_search",
    tags=["大淘客"],
    summary="超级搜索",
    description="[大淘客超级搜索](https://www.dataoke.com/pmc/api-d.html?id=14)",
    response_model=GenericItemListResponseModel,
)
async def dtk_super_search(
    g: GoodsListSuperGoodsArgs = Body(..., title="请求参数"),
    logger: BoundLogger = Depends(get_logger),
    dtk: DtkStdApi = Depends(get_dtk_std),
):
    @api_inner_wrapper(logger)
    async def inner():
        j = await dtk.goods_list_super_goods(g)
        if j is None:
            return ApiResp.from_errno(AppErrno.dtk_error)
        return ApiResp.from_data(j)

    return await inner
