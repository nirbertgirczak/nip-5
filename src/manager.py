from src.models import Apartment, Bill, Parameters, Tenant, Transfer


class Manager:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters 

        self.apartments = {}
        self.tenants = {}
        self.transfers = []
        self.bills = []
       
        self.load_data()

    def load_data(self):
        self.apartments = Apartment.from_json_file(self.parameters.apartments_json_path)
        self.tenants = Tenant.from_json_file(self.parameters.tenants_json_path)
        self.transfers = Transfer.from_json_file(self.parameters.transfers_json_path)
        self.bills = Bill.from_json_file(self.parameters.bills_json_path)

    def check_tenants_apartment_keys(self) -> bool:
        for tenant in self.tenants.values():
            if tenant.apartment not in self.apartments:
                return False
        return True
    
    # dodane przeze mnie
    def get_apartment_costs(self, apartment_key, year, month):
        apartments = {bill.get("apartment") for bill in self.bills} # mieszkanie nie istnieje
        if apartment_key not in self.apartments:
            raise ValueError
        total = 0.0
        for bill in self.bills:
            if (
                bill.get("apartment") == apartment_key and
                bill.get("settlement_year") == year and
                bill.get("settlement_month") == month
            ):
                total += bill.get("amount_pln", 0.0)
        return total