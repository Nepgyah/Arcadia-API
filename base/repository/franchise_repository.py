from base.models import Franchise

class FranchiseRepository:

    @staticmethod
    def get_franchise_by_id(id):
        try:
            return Franchise.objects.get(id=id)
        except Franchise.DoesNotExist:
            return None