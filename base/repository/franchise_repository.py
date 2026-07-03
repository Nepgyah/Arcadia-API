from base.models import Franchise

class FranchiseRepository:

    @staticmethod
    def get_franchise_by_id(franchise_id):
        try:
            return Franchise.objects.get(id=franchise_id)
        except Franchise.DoesNotExist:
            return None