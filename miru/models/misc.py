from arcadia.mixins import CompanyMixin

class AnimeCompany(CompanyMixin):
    """
        Miru specific company model to handle both producers, studios and licensors
    """

    def __str__(self):
        return f"{self.name}"