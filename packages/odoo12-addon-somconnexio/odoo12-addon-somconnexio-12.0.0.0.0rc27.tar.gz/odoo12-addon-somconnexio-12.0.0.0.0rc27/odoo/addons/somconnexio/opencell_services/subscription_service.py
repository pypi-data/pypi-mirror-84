from pyopencell.resources.subscription import Subscription

from ..opencell_models.services import ContractLineToOCServiceDict


class SubscriptionService:
    """
    Model to execute the bussines logic of Som Connexio
    working with the Subscription model of PyOpenCell
    """

    def __init__(self, contract):
        self.contract = contract

    def get(self):
        subscription_response = Subscription.get(self.contract.id)
        return subscription_response.subscription

    def terminate(self):
        subscription = self.get()
        subscription.terminate(self.contract.terminate_date.strftime("%Y-%m-%d"))

    def create_one_shot(self, product):
        subscription = self.get()

        subscription.applyOneShotCharge(product.default_code)

    def create_service(self, contract_line):
        subscription = self.get()

        opencell_service_dict = ContractLineToOCServiceDict(
            contract_line,
        ).convert()
        subscription.activate([opencell_service_dict])

    def terminate_service(self, product, termination_date):
        termination_date = termination_date.strftime("%Y-%m-%d")

        subscription = self.get()
        for service in subscription.services["serviceInstance"]:
            service_needs_update = service["code"] == product.default_code and \
                not service.get("terminationDate")
            if service_needs_update:
                subscription.terminateServices(termination_date, [service["code"]])
