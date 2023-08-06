from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr
import steam.steamid
from ..types import BrawlhallaRank, BrawlhallaTier, BrawlhallaMetal, Updatable


# noinspection PyAttributeOutsideInit
class Brawlhalla(Updatable):
    __tablename__ = "brawlhalla"

    @declared_attr
    def brawlhalla_id(self):
        return Column(Integer, primary_key=True)

    @declared_attr
    def _steamid(self):
        return Column(BigInteger, ForeignKey("steam._steamid"), unique=True)

    @declared_attr
    def steam(self):
        return relationship("Steam", backref=backref("brawlhalla", uselist=False))

    @property
    def steamid(self):
        return steam.steamid.SteamID(self._steamid)

    @declared_attr
    def name(self):
        return Column(String, nullable=False)

    @declared_attr
    def rating_1v1(self):
        return Column(Integer)

    @declared_attr
    def tier_1v1(self):
        return Column(Enum(BrawlhallaTier))

    @declared_attr
    def metal_1v1(self):
        return Column(Enum(BrawlhallaMetal))

    @property
    def rank_1v1(self):
        if self.metal_1v1 is None:
            return None
        return BrawlhallaRank(metal=self.metal_1v1, tier=self.tier_1v1)

    @rank_1v1.setter
    def rank_1v1(self, value):
        if not isinstance(value, BrawlhallaRank):
            raise TypeError("rank_1v1 can only be set to BrawlhallaRank values.")
        self.metal_1v1 = value.metal
        self.tier_1v1 = value.tier

    @property
    def duos(self):
        return [*self._duos_one, *self._duos_two]

    @property
    def rating_2v2(self):
        duos = sorted(self.duos, key=lambda d: -d.rating_2v2)
        if len(duos) == 0:
            return None
        return duos[0].rating_2v2

    @property
    def tier_2v2(self):
        duos = sorted(self.duos, key=lambda d: -d.rating_2v2)
        if len(duos) == 0:
            return None
        return duos[0].tier_2v2

    @property
    def metal_2v2(self):
        duos = sorted(self.duos, key=lambda d: -d.rating_2v2)
        if len(duos) == 0:
            return None
        return duos[0].metal_2v2

    @property
    def rank_2v2(self):
        duos = sorted(self.duos, key=lambda d: -d.rating_2v2)
        if len(duos) == 0:
            return None
        return duos[0].rank_2v2

    def json(self):
        one_rank = self.rank_1v1
        two_rank = self.rank_2v2
        return {
            "name": self.name,
            "1v1": {
                "rating": self.rating_1v1,
                "metal": one_rank.metal.name,
                "tier": one_rank.tier.name
            } if one_rank is not None else None,
            "2v2": {
                "rating": self.rating_2v2,
                "metal": two_rank.metal.name,
                "tier": two_rank.tier.name
            } if two_rank is not None else None
        }

    def __repr__(self):
        return f"<Brawlhalla account {self._steamid}>"

    def __str__(self):
        return f"[c]brawlhalla:{self.brawlhalla_id}[/c]"
