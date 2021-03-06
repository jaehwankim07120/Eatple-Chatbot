from eatple_app.apis.rest.define import *

from eatple_app.apis.rest.serializer.partner import PartnerSerializer
from eatple_app.apis.rest.serializer.store import StoreSerializer


class PartnerViewSet(viewsets.ModelViewSet):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    @swagger_auto_schema(
        operation_description="파트너",
        responses={
            200:
                PARTNER_LOGIN_200_SUCCESS.as_md(),
            400:
                PARTNER_LOGIN_300_INVALID_CRN.as_md() +
                PARTNER_LOGIN_301_INVALID_TOKEN.as_md() +
                PARTNER_LOGIN_310_NULL_CRN.as_md() +
                PARTNER_LOGIN_311_NULL_TOKEN.as_md()
        }
    )
    @action(detail=False, methods=['post'])
    def login(self, request, pk=None):
        response = {}

        try:
            json_str = ((request.body).decode('utf-8'))
            received_json_data = json.loads(json_str)

            crn = received_json_data['username'].replace('-', '')
            phone_code = received_json_data['password']
        except Exception as ex:
            print(ex)
            return JsonResponse({'status': 400, })

        if(crn == None):
            response['error_code'] = PARTNER_LOGIN_310_NULL_CRN.code
            response['error_msg'] = PARTNER_LOGIN_310_NULL_CRN.message

            return Response(response)
        elif(phone_code == None):
            response['error_code'] = PARTNER_LOGIN_311_NULL_TOKEN.code
            response['error_msg'] = PARTNER_LOGIN_311_NULL_TOKEN.message

            return Response(response)

        try:
            storeList = Store.objects.filter(crn__CRN_id=crn)
        except Store.DoesNotExist as ex:
            response['error_code'] = PARTNER_LOGIN_300_INVALID_CRN.code
            response['error_msg'] = PARTNER_LOGIN_300_INVALID_CRN.message

            return Response(response)

        phone_number_auth = False
        for store in storeList:
            checker = store.phone_number.as_national.split('-')[2]
            if(checker == phone_code):
                partnerStore = store
                phone_number_auth = True

        if(phone_number_auth == False):
            response['error_code'] = PARTNER_LOGIN_301_INVALID_TOKEN.code
            response['error_msg'] = PARTNER_LOGIN_301_INVALID_TOKEN.message

            return Response(response)

        try:
            partner = Partner.objects.get(
                phone_number=partnerStore.phone_number)
        except Partner.DoesNotExist as ex:
            partnerList = Partner.objects.filter(
                store__crn__CRN_id=partnerStore.crn.CRN_id)
            partner = partnerList.first()

        response['token'] = partner.ci
        response['token_at'] = partner.ci_authenticated_at
        response['error_code'] = PARTNER_LOGIN_200_SUCCESS.code
        response['error_msg'] = PARTNER_LOGIN_200_SUCCESS.message

        return Response(response)

    @action(detail=False, methods=['post'])
    def getProfile(self, request, pk=None):
        response = {}

        try:
            json_str = ((request.body).decode('utf-8'))
            received_json_data = json.loads(json_str)

            token = received_json_data['token']
            token_at = received_json_data['token_at']
        except Exception as ex:
            print(ex)
            return JsonResponse({'status': 400, })

        try:
            partner = Partner.objects.filter(
                ci=token,
                ci_authenticated_at=token_at,
            ).first()

            print(partner)

        except Partner.DoesNotExist as ex:
            response['error_code'] = PARTNER_LOGIN_301_INVALID_TOKEN.code
            response['error_msg'] = PARTNER_LOGIN_301_INVALID_TOKEN.message

            print(response)
            return Response(response)

        try:
            storeList = Store.objects.filter(
                crn__CRN_id=partner.store.crn.CRN_id)

        except Store.DoesNotExist as ex:
            response['error_code'] = PARTNER_LOGIN_300_INVALID_CRN.code
            response['error_msg'] = PARTNER_LOGIN_300_INVALID_CRN.message

            return Response(response)

        response['stores'] = StoreSerializer(storeList, many=True).data
        response['partner'] = PartnerSerializer(partner).data
        response['error_code'] = PARTNER_LOGIN_200_SUCCESS.code
        response['error_msg'] = PARTNER_LOGIN_200_SUCCESS.message

        return Response(response)
