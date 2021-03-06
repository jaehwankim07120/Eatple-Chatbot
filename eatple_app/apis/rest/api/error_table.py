from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions


class ErrorCollection(object):
    def __init__(self, code, status, message):
        self.code = code
        self.status = status
        self.message = message

    def as_md(self):
        return '\n\n> **%s**\n\n```\n{\n\n\t"code": "%s"\n\n\t"message": "%s"\n\n}\n\n```' % \
               (self.message, self.code, self.message)


PAYMENT_100_SUCCESS = ErrorCollection(
    code=100,
    status=status.HTTP_200_OK,
    message='결제가 완료되었습니다.'
)

PAYMENT_200_VALID = ErrorCollection(
    code=200,
    status=status.HTTP_200_OK,
    message='정상적인 주문입니다.'
)

PAYMENT_201_USER_INVALID = ErrorCollection(
    code=201,
    status=status.HTTP_200_OK,
    message='알수없는 사용자입니다. 앱으로 돌아가 다시 확인해주세요.'
)

PAYMENT_202_MULTI_ORDER = ErrorCollection(
    code=202,
    status=status.HTTP_200_OK,
    message='이미 잇플패스를 발급하셨습니다.'
)

PAYMENT_203_ORDER_ID_INVALID = ErrorCollection(
    code=203,
    status=status.HTTP_200_OK,
    message='잘못된 주문번호입니다. 홈으로가서 다시 메뉴를 선택해주세요.'
)

PAYMENT_204_ALREADY_PAID = ErrorCollection(
    code=204,
    status=status.HTTP_200_OK,
    message='이미 결제가 완료된 주문번호 입니다.'
)

PAYMENT_205_ALREADY_CANCELLED = ErrorCollection(
    code=205,
    status=status.HTTP_200_OK,
    message='이미 환불 처리된 주문번호입니다.'
)

PAYMENT_206_SELLING_TIME_INVALID = ErrorCollection(
    code=206,
    status=status.HTTP_200_OK,
    message='현재 주문 가능시간이 아닙니다.'
)

PAYMENT_600_MERCHANT_UID_INVALID = ErrorCollection(
    code=600,
    status=status.HTTP_400_BAD_REQUEST,
    message='\'merchant_uid\' is null'
)

PARTNER_LOGIN_200_SUCCESS = ErrorCollection(
    code=200,
    status=status.HTTP_200_OK,
    message='인증이 완료되었습니다.'
)

PARTNER_LOGIN_300_INVALID_CRN = ErrorCollection(
    code=300,
    status=status.HTTP_200_OK,
    message='유효하지 않은 사업자 등록번호입니다.'
)

PARTNER_LOGIN_301_INVALID_TOKEN = ErrorCollection(
    code=301,
    status=status.HTTP_200_OK,
    message='유효하지 않은 고유 번호입니다.'
)

PARTNER_LOGIN_310_NULL_CRN = ErrorCollection(
    code=310,
    status=status.HTTP_200_OK,
    message='사업자등록 번호를 입력하지 않았습니다.'
)

PARTNER_LOGIN_311_NULL_TOKEN = ErrorCollection(
    code=310,
    status=status.HTTP_200_OK,
    message='고유 번호를 입력하지 않았습니다.'
)
