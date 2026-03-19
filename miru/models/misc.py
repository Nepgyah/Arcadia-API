from base.models import Company

class AnimeCompany(Company):
    """
        Miru specific company model to handle both producers, studios and licensors
    """

    def __str__(self):
        return f"{self.name}"