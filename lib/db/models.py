from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, String, Integer, Text, JSON, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import LONGTEXT

from lib.db.database import Base

class Publication(Base):
    __tablename__ = "publications"

    id: Mapped[int] = mapped_column(primary_key=True)   

    # Identidade e tipagem
    publication_type: Mapped[Optional[str]] = mapped_column(String(100), index=True)

    # Títulos e descrição (CreativeWork)
    title: Mapped[str] = mapped_column(String(500), index=True) # title principal
    subtitle: Mapped[Optional[str]] = mapped_column(Text)
    alternative_title: Mapped[Optional[str]] = mapped_column(Text)
    abstract: Mapped[Optional[str]] = mapped_column(Text)

    # Datas (CreativeWork)
    date_published: Mapped[Optional[date]] = mapped_column(Date, index=True)

    # Idioma e classificação
    language: Mapped[Optional[str]] = mapped_column(String(35), index=True)
    subject: Mapped[Optional[str]] = mapped_column(Text)

    # Identificadores
    doi: Mapped[Optional[str]] = mapped_column(String(255), unique=True, index=True)
    isbn: Mapped[Optional[str]] = mapped_column(String(32), index=True)
    identifier: Mapped[Optional[str]] = mapped_column(String(255), index=True)

    # Publicação / acesso
    publisher: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    url: Mapped[Optional[str]] = mapped_column(Text)
    license: Mapped[Optional[str]] = mapped_column(Text)
    conditions_of_access: Mapped[Optional[str]] = mapped_column(Text)
    is_accessible_for_free: Mapped[Optional[bool]] = mapped_column(Boolean, index=True)

    # Relação com obra maior / container (CreativeWork.isPartOf)
    is_part_of_id: Mapped[Optional[int]] = mapped_column(ForeignKey("publication_containers.id"), index=True)

    # Paginação / edição / localização bibliográfica
    page_start: Mapped[Optional[str]] = mapped_column(String(50))
    page_end: Mapped[Optional[str]] = mapped_column(String(50))
    volume_number: Mapped[Optional[str]] = mapped_column(String(50))
    issue_number: Mapped[Optional[str]] = mapped_column(String(50))
    edition: Mapped[Optional[str]] = mapped_column(String(50))
    number_of_pages: Mapped[Optional[int]] = mapped_column(Integer)

    # Teses e dissertações
    in_support_of: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    source_organization: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    
    # Proviniência
    source: Mapped[Optional[str]] = mapped_column(String(50), index=True)
    raw_json: Mapped[Optional[dict]] = mapped_column(JSON)

    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    needs_review: Mapped[bool] = mapped_column(Boolean, default=False, index=True)

    container: Mapped[Optional["PublicationContainer"]] = relationship(back_populates="publications")
    contributors: Mapped[List["PublicationContributor"]] = relationship(back_populates="publication", cascade="all, delete-orphan")
    fundings: Mapped[List["PublicationFunder"]] = relationship(back_populates="publication", cascade="all, delete-orphan")
    keywords: Mapped[List["PublicationKeyword"]] = relationship(back_populates="publication", cascade="all, delete-orphan")
    metrics: Mapped[Optional["PublicationMetric"]] = relationship(back_populates="publication", cascade="all, delete-orphan")
    
    outgoing_references: Mapped[List["PublicationReference"]] = relationship(
        foreign_keys="PublicationReference.citing_publication_id",
        back_populates="citing_publication",
        cascade="all, delete-orphan"
    )
    incoming_references: Mapped[List["PublicationReference"]] = relationship(
    foreign_keys="PublicationReference.cited_publication_id",
    back_populates="cited_publication"
)
    
class PublicationReference(Base):
    __tablename__ = "publication_references"
    __table_args__ = (
        UniqueConstraint(
            "citing_publication_id",
            "position",
            name="uq_publication_reference_position"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    # artigo que está citando
    citing_publication_id: Mapped[int] = mapped_column(
        ForeignKey("publications.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # artigo citado, se já existir no banco
    cited_publication_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("publications.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    position: Mapped[int] = mapped_column(Integer, nullable=False)

    # dados brutos / parciais da referência
    doi: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    title: Mapped[Optional[str]] = mapped_column(Text)
    author: Mapped[Optional[str]] = mapped_column(Text)
    journal_title: Mapped[Optional[str]] = mapped_column(Text)
    year: Mapped[Optional[str]] = mapped_column(String(10), index=True)
    volume: Mapped[Optional[str]] = mapped_column(String(50))
    issue: Mapped[Optional[str]] = mapped_column(String(50))


    # status de resolução
    match_source: Mapped[Optional[str]] = mapped_column(String(50))  

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    citing_publication: Mapped["Publication"] = relationship(
        foreign_keys=[citing_publication_id],
        back_populates="outgoing_references"
    )

    cited_publication: Mapped[Optional["Publication"]] = relationship(
    foreign_keys=[cited_publication_id],
    back_populates="incoming_references"
)

class PublicationContainer(Base):
    __tablename__ = "publication_containers"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(500), index=True)
    alternate_name: Mapped[Optional[str]] = mapped_column(String(255))
    publisher: Mapped[Optional[str]] = mapped_column(String(255), index=True)

    issn_print: Mapped[Optional[str]] = mapped_column(String(20), index=True)
    issn_electronic: Mapped[Optional[str]] = mapped_column(String(20), index=True)
    isbn: Mapped[Optional[str]] = mapped_column(String(32), index=True)

    url: Mapped[Optional[str]] = mapped_column(Text)

    publications: Mapped[List["Publication"]] = relationship(back_populates="container")
       
class PublicationContributor(Base):
    __tablename__ = "publication_contributors"

    id: Mapped[int] = mapped_column(primary_key=True)
    publication_id: Mapped[int] = mapped_column(ForeignKey("publications.id"), index=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), index=True)

    role: Mapped[Optional[str]] = mapped_column(String(50), index=True)  # author, editor, organizer, advisor
    position: Mapped[Optional[str]] = mapped_column(String(50), index=True) 

    raw_name: Mapped[Optional[str]] = mapped_column(String(255))
    raw_affiliation: Mapped[Optional[str]] = mapped_column(Text)

    publication: Mapped["Publication"] = relationship(back_populates="contributors")
    author: Mapped["Author"] = relationship(back_populates="authorships")
    affiliations: Mapped[List["PublicationContributorAffiliation"]] = relationship(
        back_populates="publication_contributor",
        cascade="all, delete-orphan"
    )
    
class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)

    full_name: Mapped[str] = mapped_column(String(255), index=True)
    given_name: Mapped[Optional[str]] = mapped_column(String(255))
    family_name: Mapped[Optional[str]] = mapped_column(String(255))
    orcid: Mapped[Optional[str]] = mapped_column(String(50), unique=True, index=True)
    lattes_id: Mapped[Optional[str]] = mapped_column(String(50), unique=True, index=True)
    is_inpa_researcher: Mapped[Optional[bool]] = mapped_column(Boolean, index=True)
    normalized_full_name: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    canonical_source: Mapped[Optional[str]] = mapped_column(String(50))
    needs_review: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    
    affiliation_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("affiliations.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    
    affiliation: Mapped[Optional["Affiliation"]] = relationship(
        "Affiliation",
        back_populates="authors"
    )

    authorships: Mapped[List["PublicationContributor"]] = relationship(
        back_populates="author"
    )

    lattes_profile: Mapped[Optional["Lattes"]] = relationship(
        "Lattes",
        back_populates="author",
        uselist=False,
        cascade="all, delete-orphan",
        single_parent=True
    )
     
class Lattes(Base):
    __tablename__ = "lattes"

    id: Mapped[int] = mapped_column(primary_key=True)

    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True
    )

    lattes_id: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    lattes_update: Mapped[datetime] = mapped_column(DateTime)
    html: Mapped[str] = mapped_column(LONGTEXT)
    # json: Mapped[dict] = mapped_column(JSON)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    author: Mapped["Author"] = relationship(
        "Author",
        back_populates="lattes_profile"
    )
    
class Funder(Base):
    __tablename__ = "funders"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    standard_name: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    acronym: Mapped[Optional[str]] = mapped_column(String(50), index=True)
    doi: Mapped[Optional[str]] = mapped_column(String(255), unique=True, index=True)
    country: Mapped[Optional[str]] = mapped_column(String(100))
       
class PublicationFunder(Base):
    __tablename__ = "publication_funders"
    __table_args__ = (
        UniqueConstraint(
            "publication_id",
            "funder_id",
            "award_number",
            name="uq_publication_funder_award"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    publication_id: Mapped[int] = mapped_column(ForeignKey("publications.id"), index=True)
    funder_id: Mapped[int] = mapped_column(ForeignKey("funders.id"), index=True)
    award_number: Mapped[Optional[str]] = mapped_column(String(255), index=True)

    publication: Mapped["Publication"] = relationship(back_populates="fundings")
    funder: Mapped["Funder"] = relationship()
    
class PublicationKeyword(Base):
    __tablename__ = "publication_keywords"
    __table_args__ = (
        UniqueConstraint(
            "publication_id",
            "normalized_keyword",
            "language",
            name="uq_publication_keyword_norm_lang"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    publication_id: Mapped[int] = mapped_column(ForeignKey("publications.id"), index=True)
    keyword: Mapped[str] = mapped_column(String(255), index=True)
    normalized_keyword: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    language: Mapped[Optional[str]] = mapped_column(String(20))
    source: Mapped[Optional[str]] = mapped_column(String(50))

    publication: Mapped["Publication"] = relationship(back_populates="keywords")
    
class PublicationMetric(Base):
    __tablename__ = "metrics"

    id: Mapped[int] = mapped_column(primary_key=True)
    publication_id: Mapped[int] = mapped_column(ForeignKey("publications.id"), index=True)

    collected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    citation_count: Mapped[Optional[int]] = mapped_column(Integer)
    reference_count: Mapped[Optional[int]] = mapped_column(Integer)
    altmetric_score: Mapped[Optional[float]] = mapped_column()
    mendeley_readers: Mapped[Optional[int]] = mapped_column(Integer)
    tweets_count: Mapped[Optional[int]] = mapped_column(Integer)
    news_count: Mapped[Optional[int]] = mapped_column(Integer)
    blog_count: Mapped[Optional[int]] = mapped_column(Integer)
    policy_count: Mapped[Optional[int]] = mapped_column(Integer)
    patent_count: Mapped[Optional[int]] = mapped_column(Integer)

    source: Mapped[Optional[str]] = mapped_column(String(50), index=True)

    publication: Mapped["Publication"] = relationship(back_populates="metrics")
    
class PublicationContributorAffiliation(Base):
    __tablename__ = "publication_contributor_affiliations"
    __table_args__ = (
        UniqueConstraint(
            "publication_contributor_id",
            "affiliation_id",
            name="uq_pub_contrib_affiliation"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    publication_contributor_id: Mapped[int] = mapped_column(
        ForeignKey("publication_contributors.id"), index=True
    )
    affiliation_id: Mapped[int] = mapped_column(
        ForeignKey("affiliations.id"), index=True
    )

    publication_contributor: Mapped["PublicationContributor"] = relationship(
        back_populates="affiliations"
    )
    affiliation: Mapped["Affiliation"] = relationship()
    
class Affiliation(Base):
    __tablename__ = "affiliations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(500), index=True)
    standard_name: Mapped[Optional[str]] = mapped_column(String(500), index=True)
    acronym: Mapped[Optional[str]] = mapped_column(String(50), index=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    state: Mapped[Optional[str]] = mapped_column(String(100))
    city: Mapped[Optional[str]] = mapped_column(String(100))
    
    authors: Mapped[List["Author"]] = relationship(
        "Author",
        back_populates="affiliation"
    )