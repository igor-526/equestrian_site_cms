from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from random import Random
from typing import Any, Sequence
from uuid import UUID

from sqlalchemy import delete, insert, select
from sqlalchemy.orm import Session

from core.entities.statistic import EntityTypeForStatistic, StatisticFieldType
from core.seeds.statistic_filter_field import (
    FILTER_FIELD_COUNTRY_ID,
    FILTER_FIELD_DEVICE_TYPE,
    FILTER_FIELD_TRAFFIC_SOURCE,
)
from models import (
    clusters,
    pages,
    projects,
    queries,
    statistic_fields,
    statistic_filter_fields,
    statistic_filter_values,
    statistic_top_options,
    statistic_value_to_filter_values,
    statistic_values,
    users,
)
from utils.database import SyncSession
from utils.security import Security

DEMO_OWNER_USERNAME = "demo_owner"
DEMO_OWNER_PASSWORD = "demo1234"
DEMO_OWNER_FIRST_NAME = "Demo"
DEMO_OWNER_LAST_NAME = "Owner"


@dataclass(frozen=True)
class ClusterTemplate:
    name: str
    description: str
    keywords: tuple[str, ...]
    anchor_paths: tuple[str, ...] = ()


@dataclass(frozen=True)
class ProjectTemplate:
    name: str
    description: str
    domain: str
    has_https: bool
    is_subdomain: bool
    page_paths: tuple[str, ...]
    queries: tuple[str, ...]
    cluster_templates: tuple[ClusterTemplate, ...]
    competitor_domains: tuple[str, ...]


@dataclass(frozen=True)
class FieldSeriesConfig:
    abbreviation: str
    entity_type: EntityTypeForStatistic
    expected_type: StatisticFieldType
    base_range: tuple[float, float]
    trend_range: tuple[float, float]
    noise: float
    decimals: int | None = None
    minimum: float | None = None
    maximum: float | None = None


@dataclass(frozen=True)
class PageRecord:
    id: UUID
    path: str
    url: str
    is_competitor: bool


@dataclass(frozen=True)
class ClusterRecord:
    id: UUID
    name: str
    keywords: tuple[str, ...]


@dataclass(frozen=True)
class QueryRecord:
    id: UUID
    text: str


@dataclass(frozen=True)
class FieldMetadata:
    id: UUID
    type: StatisticFieldType


@dataclass(frozen=True)
class TopOptionTemplate:
    option_id: str
    label: str
    short_label: str
    order: int
    limit_value: int | None = None
    value_from: float | None = None
    value_to: float | None = None


@dataclass(frozen=True)
class StatisticFilterCombination:
    device_type_id: UUID
    traffic_source_id: UUID


@dataclass(frozen=True)
class StatisticFilterPool:
    combinations: tuple[StatisticFilterCombination, ...]
    country_id: UUID


FILTER_COMBINATIONS_FOR_DEMO: tuple[tuple[str, str], ...] = (
    ("Компьютеры", "Поисковая система Яндекс"),
    ("Телефоны", "Поисковая система Google"),
)
COUNTRY_NAME_FOR_DEMO = "Россия"

KEY_METRIC_ABBREVIATIONS: tuple[str, ...] = ("PIM", "PCL", "QIM", "QCL")
SYSTEM_TOP_OPTION_TEMPLATES: tuple[TopOptionTemplate, ...] = (
    TopOptionTemplate(
        option_id="all",
        label="Все",
        short_label="Все",
        order=1,
    ),
    TopOptionTemplate(
        option_id="top10",
        label="Топ 10",
        short_label="1-10",
        order=2,
        limit_value=10,
    ),
    TopOptionTemplate(
        option_id="top30",
        label="Топ 30",
        short_label="1-30",
        order=3,
        limit_value=30,
    ),
)


PROJECT_TEMPLATES: tuple[ProjectTemplate, ...] = (
    ProjectTemplate(
        name="Aurora Commerce",
        description=(
            "Интернет-магазин товаров для устойчивого образа жизни: бутылки, кухонные аксессуары, наборы zero waste."
        ),
        domain="aurora-commerce.demo",
        has_https=True,
        is_subdomain=False,
        page_paths=(
            "",
            "catalog",
            "catalog/new-arrivals",
            "catalog/bestsellers",
            "catalog/eco-kits",
            "catalog/gifts",
            "catalog/zero-waste",
            "product/eco-bottle",
            "product/coffee-cup",
            "product/reusable-straws",
            "product/bamboo-toothbrush",
            "product/recycled-notebook",
            "guides/sustainable-living",
            "blog",
            "blog/recycling-basics",
            "blog/zero-waste-kitchen",
            "blog/green-office",
            "about",
            "about/mission",
            "support/shipping",
            "support/returns",
            "guides/gift-ideas",
        ),
        queries=(
            "купить эко бутылку",
            "многоразовая бутылка стеклянная",
            "бамбуковая зубная щетка",
            "zero waste набор купить",
            "многоразовые трубочки стальные",
            "подарочный набор эко товары",
            "эко подарки для офиса",
            "перерабатываемые блокноты",
            "многоразовая кружка для кофе",
            "экологичная посуда для пикника",
            "органические чистящие средства",
            "эко подарки на новый год",
            "как начать zero waste дома",
            "сумка шоппер хлопковая",
            "набор для сортировки мусора",
            "многоразовые пакеты для овощей",
            "экологичные подарки для коллег",
            "компостер для квартиры купить",
            "советы по осознанным покупкам",
            "экологичная доставка продуктов",
            "интернет магазин экотоваров",
            "эко аксессуары для кухни",
        ),
        cluster_templates=(
            ClusterTemplate(
                name="Zero Waste Starter Kits",
                description="Комплекты для начала осознанного потребления",
                keywords=("zero waste", "набор"),
                anchor_paths=("catalog/zero-waste", "guides/sustainable-living"),
            ),
            ClusterTemplate(
                name="Reusable Drinkware",
                description="Многоразовые бутылки, кружки и стаканы",
                keywords=("бутыл", "кружк", "термос", "стакан"),
                anchor_paths=("product/eco-bottle", "product/coffee-cup"),
            ),
            ClusterTemplate(
                name="Eco Gifts",
                description="Подарочные наборы и идеи для праздников",
                keywords=("подар",),
                anchor_paths=("catalog/gifts", "guides/gift-ideas"),
            ),
            ClusterTemplate(
                name="Home Cleaning",
                description="Экологичные средства для уборки дома",
                keywords=("чист", "уборк"),
                anchor_paths=("catalog/eco-kits",),
            ),
            ClusterTemplate(
                name="Office Sustainability",
                description="Решения для экологичного офиса",
                keywords=("офис", "коллег"),
                anchor_paths=("blog/green-office",),
            ),
            ClusterTemplate(
                name="Travel Essentials",
                description="Удобные вещи для путешествий без отходов",
                keywords=("путеше", "дорог"),
                anchor_paths=("catalog/bestsellers",),
            ),
            ClusterTemplate(
                name="Composting Solutions",
                description="Компостеры и всё для переработки органики дома",
                keywords=("компост",),
                anchor_paths=("blog/recycling-basics",),
            ),
            ClusterTemplate(
                name="Kitchen Swaps",
                description="Замены для кухни без пластика",
                keywords=("кухн", "посуд"),
                anchor_paths=("blog/zero-waste-kitchen",),
            ),
            ClusterTemplate(
                name="Storage and Bags",
                description="Мешочки и сумки многоразового использования",
                keywords=("сумк", "пакет"),
                anchor_paths=("catalog/new-arrivals",),
            ),
            ClusterTemplate(
                name="Recycling Education",
                description="Материалы по сортировке и переработке",
                keywords=("переработ", "совет"),
                anchor_paths=("guides/sustainable-living",),
            ),
        ),
        competitor_domains=(
            "eco-market.example",
            "greenliving.shop",
            "zerowaste-store.test",
        ),
    ),
    ProjectTemplate(
        name="GreenPulse Energy",
        description=(
            "Решения по солнечной генерации для домов и бизнеса, мониторинг и обслуживание энергетической инфраструктуры."
        ),
        domain="grid.greenpulse.demo",
        has_https=True,
        is_subdomain=True,
        page_paths=(
            "",
            "solutions",
            "solutions/solar-panels",
            "solutions/solar-rooftop",
            "solutions/battery-storage",
            "solutions/charging-stations",
            "solutions/microgrid",
            "case-studies",
            "case-studies/residential-solar",
            "case-studies/commercial-solar",
            "case-studies/microgrid",
            "blog",
            "blog/solar-incentives",
            "blog/energy-monitoring",
            "blog/maintenance-checklist",
            "insights/roi-calculator",
            "about",
            "about/team",
            "about/partners",
            "support/consultation",
            "support/maintenance",
            "webinars/energy-audit",
        ),
        queries=(
            "солнечные панели для дома",
            "подбор солнечной станции",
            "энергетический аудит предприятия",
            "монтаж солнечных панелей цена",
            "обслуживание солнечных батарей",
            "аккумулятор для солнечной электростанции",
            "зарядные станции для электромобилей",
            "коммерческая солнечная энергетика",
            "микрогрид решения",
            "инвестиции в солнечную генерацию",
            "субсидии на солнечные панели",
            "расчет окупаемости солнечной станции",
            "дистанционный мониторинг энергии",
            "солнечные панели для офиса",
            "солнечные панели для склада",
            "домашняя солнечная электростанция",
            "как выбрать инвертор",
            "оптимизация энергопотребления",
            "зеленые тарифы для бизнеса",
            "шум солнечных батарей",
            "подключение солнечных панелей к сети",
            "хранение энергии для бизнеса",
        ),
        cluster_templates=(
            ClusterTemplate(
                name="Residential Solar",
                description="Проекты для частных домов и таунхаусов",
                keywords=("дом", "кварт", "residential"),
                anchor_paths=(
                    "case-studies/residential-solar",
                    "solutions/solar-rooftop",
                ),
            ),
            ClusterTemplate(
                name="Commercial Solar",
                description="Генерация энергии для бизнеса",
                keywords=("бизнес", "офис", "склад", "коммер"),
                anchor_paths=("case-studies/commercial-solar",),
            ),
            ClusterTemplate(
                name="Energy Storage",
                description="Накопители энергии и аккумуляторные системы",
                keywords=("аккум", "storage"),
                anchor_paths=("solutions/battery-storage",),
            ),
            ClusterTemplate(
                name="EV Charging",
                description="Инфраструктура для электромобилей",
                keywords=("заряд", "ev", "электромоб"),
                anchor_paths=("solutions/charging-stations",),
            ),
            ClusterTemplate(
                name="Microgrid Projects",
                description="Автономные энергосистемы и микрогриды",
                keywords=("микр", "microgrid"),
                anchor_paths=("solutions/microgrid", "case-studies/microgrid"),
            ),
            ClusterTemplate(
                name="Financial Planning",
                description="Окупаемость и тарифы",
                keywords=("окуп", "инвести", "тариф"),
                anchor_paths=("insights/roi-calculator", "blog/solar-incentives"),
            ),
            ClusterTemplate(
                name="Operations & Maintenance",
                description="Обслуживание и мониторинг",
                keywords=("обслуж", "монитор", "maintenance"),
                anchor_paths=("blog/maintenance-checklist", "support/maintenance"),
            ),
            ClusterTemplate(
                name="Consulting",
                description="Экспертные консультации и энергоаудит",
                keywords=("аудит", "консультац"),
                anchor_paths=("support/consultation", "webinars/energy-audit"),
            ),
            ClusterTemplate(
                name="Regulatory Support",
                description="Помощь с зелеными тарифами и субсидиями",
                keywords=("субсид", "тариф"),
                anchor_paths=("blog/solar-incentives",),
            ),
            ClusterTemplate(
                name="Smart Monitoring",
                description="Цифровые сервисы мониторинга энергии",
                keywords=("монитор", "дистан"),
                anchor_paths=("blog/energy-monitoring",),
            ),
        ),
        competitor_domains=(
            "sunpeak.energy",
            "helio-tech.example",
            "bright-grid.io",
        ),
    ),
    ProjectTemplate(
        name="Skyward Travels",
        description=(
            "Туристическое агентство с акцентом на авторские путешествия, активный отдых и сезонные туры."
        ),
        domain="skyward-travels.demo",
        has_https=True,
        is_subdomain=False,
        page_paths=(
            "",
            "destinations",
            "destinations/europe/alps",
            "destinations/europe/scandinavia",
            "destinations/asia/japan",
            "destinations/asia/vietnam",
            "destinations/america/patagonia",
            "destinations/america/canada",
            "destinations/polar/iceland",
            "tours/winter",
            "tours/summer",
            "tours/family",
            "tours/adventure",
            "blog",
            "blog/winter-hiking",
            "blog/travel-gear",
            "blog/food-guides",
            "guides/visa-support",
            "guides/packing-list",
            "about",
            "about/team",
            "support/faq",
            "support/insurance",
        ),
        queries=(
            "туры в альпы зимой",
            "горнолыжные туры из москвы",
            "летние авторские туры",
            "путешествие по патогонии",
            "экскурсии в исландии",
            "тур по скандинавии",
            "семейные туры летом",
            "туры для начинающих хайкеров",
            "как подготовиться к треккингу",
            "тур по японии сакура",
            "туры во вьетнам с гидом",
            "страховка для активного отдыха",
            "групповой тур в канаду",
            "что взять в поход зимой",
            "экспедиционные туры",
            "туры выходного дня",
            "как выбрать туристическое снаряжение",
            "туры на северное сияние",
            "круизы по фьордам",
            "туры в горы с детьми",
            "осенние гастрономические туры",
            "авторские туры на байкал",
        ),
        cluster_templates=(
            ClusterTemplate(
                name="Winter Adventures",
                description="Зимние туры и экспедиции",
                keywords=("зим", "снег", "лыж", "сиян"),
                anchor_paths=("tours/winter", "blog/winter-hiking"),
            ),
            ClusterTemplate(
                name="Summer Escapes",
                description="Летние маршруты и отдых у моря",
                keywords=("летн", "пляж"),
                anchor_paths=("tours/summer",),
            ),
            ClusterTemplate(
                name="Family Journeys",
                description="Путешествия для семей с детьми",
                keywords=("семей", "дет"),
                anchor_paths=("tours/family",),
            ),
            ClusterTemplate(
                name="Asia Discovery",
                description="Программы по Азии",
                keywords=("япон", "вьет", "азия"),
                anchor_paths=("destinations/asia/japan", "destinations/asia/vietnam"),
            ),
            ClusterTemplate(
                name="Nordic Highlights",
                description="Скандинавия и страны севера",
                keywords=("сканд", "норв", "фьорд", "сиян"),
                anchor_paths=(
                    "destinations/europe/scandinavia",
                    "destinations/polar/iceland",
                ),
            ),
            ClusterTemplate(
                name="Americas Expeditions",
                description="Маршруты по Северной и Южной Америке",
                keywords=("патаг", "канад", "амер"),
                anchor_paths=(
                    "destinations/america/patagonia",
                    "destinations/america/canada",
                ),
            ),
            ClusterTemplate(
                name="Gear & Preparation",
                description="Подготовка к походам и подбор снаряжения",
                keywords=("снаряж", "подготов", "взять"),
                anchor_paths=("blog/travel-gear", "guides/packing-list"),
            ),
            ClusterTemplate(
                name="Culinary Routes",
                description="Гастрономические путешествия",
                keywords=("гастр", "еда", "food"),
                anchor_paths=("blog/food-guides",),
            ),
            ClusterTemplate(
                name="Weekend Trips",
                description="Короткие поездки и туры выходного дня",
                keywords=("выход", "уикенд"),
                anchor_paths=("tours/adventure",),
            ),
            ClusterTemplate(
                name="Logistics & Support",
                description="Визы, страховки и поддержка",
                keywords=("виза", "страх", "поддерж"),
                anchor_paths=("guides/visa-support", "support/insurance"),
            ),
        ),
        competitor_domains=(
            "northernlights.travel",
            "alpine-adventures.example",
            "family-escape.tours",
        ),
    ),
)


FIELD_SERIES_CONFIGS: tuple[FieldSeriesConfig, ...] = (
    FieldSeriesConfig(
        abbreviation="PIM",
        entity_type=EntityTypeForStatistic.page,
        expected_type=StatisticFieldType.integer,
        base_range=(900, 3200),
        trend_range=(35, 110),
        noise=140,
        minimum=100,
    ),
    FieldSeriesConfig(
        abbreviation="PCL",
        entity_type=EntityTypeForStatistic.page,
        expected_type=StatisticFieldType.integer,
        base_range=(120, 420),
        trend_range=(8, 22),
        noise=25,
        minimum=20,
    ),
    FieldSeriesConfig(
        abbreviation="PCR",
        entity_type=EntityTypeForStatistic.page,
        expected_type=StatisticFieldType.float,
        base_range=(2.1, 5.8),
        trend_range=(-0.15, 0.12),
        noise=0.35,
        decimals=2,
        minimum=0.8,
        maximum=9.0,
    ),
    FieldSeriesConfig(
        abbreviation="VST",
        entity_type=EntityTypeForStatistic.page,
        expected_type=StatisticFieldType.float,
        base_range=(210, 640),
        trend_range=(18, 55),
        noise=45,
        decimals=1,
        minimum=50,
    ),
    FieldSeriesConfig(
        abbreviation="CVR",
        entity_type=EntityTypeForStatistic.page,
        expected_type=StatisticFieldType.float,
        base_range=(0.9, 2.8),
        trend_range=(-0.08, 0.05),
        noise=0.12,
        decimals=2,
        minimum=0.4,
        maximum=4.5,
    ),
    FieldSeriesConfig(
        abbreviation="WS",
        entity_type=EntityTypeForStatistic.page,
        expected_type=StatisticFieldType.integer,
        base_range=(160, 520),
        trend_range=(6, 24),
        noise=28,
        minimum=0,
    ),
    FieldSeriesConfig(
        abbreviation="QIM",
        entity_type=EntityTypeForStatistic.query,
        expected_type=StatisticFieldType.integer,
        base_range=(1100, 4200),
        trend_range=(45, 160),
        noise=120,
        minimum=80,
    ),
    FieldSeriesConfig(
        abbreviation="QDM",
        entity_type=EntityTypeForStatistic.query,
        expected_type=StatisticFieldType.float,
        base_range=(120.0, 620.0),
        trend_range=(8.0, 22.0),
        noise=28.0,
        decimals=1,
        minimum=20.0,
    ),
    FieldSeriesConfig(
        abbreviation="QCL",
        entity_type=EntityTypeForStatistic.query,
        expected_type=StatisticFieldType.integer,
        base_range=(70, 320),
        trend_range=(4, 16),
        noise=18,
        minimum=5,
    ),
    FieldSeriesConfig(
        abbreviation="QCR",
        entity_type=EntityTypeForStatistic.query,
        expected_type=StatisticFieldType.float,
        base_range=(2.4, 8.5),
        trend_range=(-0.2, 0.18),
        noise=0.42,
        decimals=2,
        minimum=0.6,
        maximum=12.0,
    ),
    FieldSeriesConfig(
        abbreviation="VSTQ",
        entity_type=EntityTypeForStatistic.query,
        expected_type=StatisticFieldType.float,
        base_range=(45, 210),
        trend_range=(6, 18),
        noise=12,
        decimals=1,
        minimum=10,
    ),
    FieldSeriesConfig(
        abbreviation="CVRQ",
        entity_type=EntityTypeForStatistic.query,
        expected_type=StatisticFieldType.float,
        base_range=(0.8, 3.6),
        trend_range=(-0.06, 0.04),
        noise=0.08,
        decimals=2,
        minimum=0.2,
        maximum=4.2,
    ),
    FieldSeriesConfig(
        abbreviation="WS",
        entity_type=EntityTypeForStatistic.query,
        expected_type=StatisticFieldType.integer,
        base_range=(350, 2100),
        trend_range=(18, 90),
        noise=75,
        minimum=0,
    ),
)


def ensure_demo_owner(*, session: Session, security: Security) -> UUID:
    """Return identifier of the demo user, creating it when missing."""

    user_row = (
        session.execute(
            select(users.c.id).where(users.c.username == DEMO_OWNER_USERNAME)
        )
        .scalars()
        .first()
    )
    if user_row:
        return user_row

    hashed_password = security.hash_password(DEMO_OWNER_PASSWORD)
    created_user = (
        session.execute(
            insert(users)
            .values(
                username=DEMO_OWNER_USERNAME,
                password=hashed_password,
                first_name=DEMO_OWNER_FIRST_NAME,
                last_name=DEMO_OWNER_LAST_NAME,
            )
            .returning(users.c.id)
        )
        .scalars()
        .one()
    )
    print("Создан пользователь", DEMO_OWNER_USERNAME, "с паролем", DEMO_OWNER_PASSWORD)
    return created_user


def clear_existing_demo_projects(
    *, session: Session, project_names: Sequence[str]
) -> None:
    """Remove previously generated demo data to keep the script idempotent."""

    if not project_names:
        return

    existing_project_ids = (
        session.execute(select(projects.c.id).where(projects.c.name.in_(project_names)))
        .scalars()
        .all()
    )
    if not existing_project_ids:
        return

    page_ids = (
        session.execute(
            select(pages.c.id).where(pages.c.project_id.in_(existing_project_ids))
        )
        .scalars()
        .all()
    )
    if page_ids:
        session.execute(
            delete(statistic_values).where(
                (statistic_values.c.entity_type == EntityTypeForStatistic.page.value)
                & (statistic_values.c.entity_id.in_(page_ids))
            )
        )

    query_ids = (
        session.execute(
            select(queries.c.id).where(queries.c.project_id.in_(existing_project_ids))
        )
        .scalars()
        .all()
    )
    if query_ids:
        session.execute(
            delete(statistic_values).where(
                (statistic_values.c.entity_type == EntityTypeForStatistic.query.value)
                & (statistic_values.c.entity_id.in_(query_ids))
            )
        )

    session.execute(
        delete(queries).where(queries.c.project_id.in_(existing_project_ids))
    )
    session.execute(
        delete(clusters).where(clusters.c.project_id.in_(existing_project_ids))
    )
    session.execute(delete(pages).where(pages.c.project_id.in_(existing_project_ids)))
    session.execute(delete(projects).where(projects.c.id.in_(existing_project_ids)))


def create_project(
    *, session: Session, template: ProjectTemplate, owner_id: UUID, rng: Random
) -> UUID:
    """Insert project row and return its identifier."""

    project_id = (
        session.execute(
            insert(projects)
            .values(
                name=template.name,
                description=template.description,
                domain=template.domain,
                has_https=template.has_https,
                is_subdomain=template.is_subdomain,
                owner_id=owner_id,
            )
            .returning(projects.c.id)
        )
        .scalars()
        .one()
    )
    print(f"Создан проект '{template.name}' с доменом {template.domain}")
    return project_id


def build_page_url(*, domain: str, path: str, has_https: bool) -> str:
    scheme = "https" if has_https else "http"
    clean_path = path.strip("/")
    if not clean_path:
        return f"{scheme}://{domain}/"
    return f"{scheme}://{domain}/{clean_path}"


def create_pages_for_project(
    *,
    session: Session,
    template: ProjectTemplate,
    project_id: UUID,
    rng: Random,
) -> list[PageRecord]:
    """Create a pool of pages for the project."""

    desired_count = rng.randint(10, min(15, len(template.page_paths)))
    selected_paths = list(template.page_paths)
    rng.shuffle(selected_paths)
    selected_paths = selected_paths[:desired_count]

    records: list[PageRecord] = []
    has_competitors = bool(template.competitor_domains)

    for path in selected_paths:
        is_competitor = has_competitors and rng.random() < 0.2
        domain = (
            rng.choice(template.competitor_domains)
            if is_competitor
            else template.domain
        )
        use_https = True if is_competitor else template.has_https
        url = build_page_url(domain=domain, path=path, has_https=use_https)
        inserted_page = (
            session.execute(
                insert(pages)
                .values(
                    url_full=url,
                    is_competitor=is_competitor,
                    project_id=project_id,
                )
                .returning(pages.c.id, pages.c.url_full)
            )
            .mappings()
            .one()
        )
        records.append(
            PageRecord(
                id=inserted_page["id"],
                path=path.strip("/"),
                url=inserted_page["url_full"],
                is_competitor=is_competitor,
            )
        )
    return records


def choose_anchor_page(
    *, pages_pool: Sequence[PageRecord], anchors: Sequence[str], rng: Random
) -> PageRecord:
    normalized = {page.path: page for page in pages_pool}
    for anchor in anchors:
        key = anchor.strip("/")
        if key in normalized:
            return normalized[key]
    return rng.choice(pages_pool)


def create_clusters_for_project(
    *,
    session: Session,
    template: ProjectTemplate,
    project_id: UUID,
    pages_pool: Sequence[PageRecord],
    rng: Random,
) -> list[ClusterRecord]:
    """Create thematic clusters tied to the project."""

    max_count = min(len(template.cluster_templates), 10)
    desired_count = rng.randint(5, max_count)
    candidates = list(template.cluster_templates)
    rng.shuffle(candidates)
    selected_templates = candidates[:desired_count]

    clusters_created: list[ClusterRecord] = []
    for cluster_template in selected_templates:
        anchor_page = choose_anchor_page(
            pages_pool=pages_pool,
            anchors=cluster_template.anchor_paths,
            rng=rng,
        )
        row = (
            session.execute(
                insert(clusters)
                .values(
                    name=cluster_template.name,
                    description=cluster_template.description,
                    project_id=project_id,
                    page_id=anchor_page.id,
                )
                .returning(clusters.c.id, clusters.c.name)
            )
            .mappings()
            .one()
        )
        clusters_created.append(
            ClusterRecord(
                id=row["id"],
                name=row["name"],
                keywords=cluster_template.keywords,
            )
        )
    return clusters_created


def pick_cluster_for_query(
    *,
    query_text: str,
    clusters_pool: Sequence[ClusterRecord],
    rng: Random,
) -> ClusterRecord:
    lower_query = query_text.lower()
    matching = [
        cluster
        for cluster in clusters_pool
        if any(keyword in lower_query for keyword in cluster.keywords)
    ]
    return rng.choice(matching or list(clusters_pool))


def create_queries_for_project(
    *,
    session: Session,
    template: ProjectTemplate,
    project_id: UUID,
    clusters_pool: Sequence[ClusterRecord],
    rng: Random,
) -> list[QueryRecord]:
    """Create queries distributed across clusters."""

    max_count = min(len(template.queries), 20)
    desired_count = rng.randint(15, max_count)
    candidate_queries = list(template.queries)
    rng.shuffle(candidate_queries)
    selected_queries = candidate_queries[:desired_count]

    records: list[QueryRecord] = []
    for query_text in selected_queries:
        cluster = pick_cluster_for_query(
            query_text=query_text, clusters_pool=clusters_pool, rng=rng
        )
        row = (
            session.execute(
                insert(queries)
                .values(
                    query=query_text,
                    project_id=project_id,
                    cluster_id=cluster.id,
                )
                .returning(queries.c.id, queries.c.query)
            )
            .mappings()
            .one()
        )
        records.append(QueryRecord(id=row["id"], text=row["query"]))
    return records


def generate_recorded_dates(*, days: int) -> list[datetime]:
    base = datetime.now(timezone.utc).replace(
        hour=11, minute=0, second=0, microsecond=0
    )
    return [base - timedelta(days=delta) for delta in range(days - 1, -1, -1)]


def load_field_metadata(
    *, session: Session, configs: Sequence[FieldSeriesConfig]
) -> dict[str, FieldMetadata]:
    abbreviations = {config.abbreviation for config in configs}
    stmt = select(
        statistic_fields.c.abbreviation,
        statistic_fields.c.id,
        statistic_fields.c.type,
        statistic_fields.c.aggregation,
    ).where(statistic_fields.c.abbreviation.in_(abbreviations))

    rows = session.execute(stmt).mappings().all()
    metadata: dict[str, FieldMetadata] = {}
    for row in rows:
        abbreviation = row["abbreviation"]
        field_type = StatisticFieldType(row["type"])
        aggregation: dict[str, Any] = row["aggregation"] or {}
        metadata[abbreviation] = FieldMetadata(id=row["id"], type=field_type)
        config = next(
            config for config in configs if config.abbreviation == abbreviation
        )
        if field_type is not config.expected_type:
            raise RuntimeError(
                f"Поле {abbreviation} имеет тип {field_type}, ожидается {config.expected_type}"
            )
        if config.entity_type.value not in aggregation:
            raise RuntimeError(
                f"Поле {abbreviation} не поддерживает сущность {config.entity_type.value}"
            )

    if abbreviations - metadata.keys():
        missing = ", ".join(sorted(abbreviations - metadata.keys()))
        raise RuntimeError(f"Не найдены поля статистики: {missing}")

    return metadata


def ensure_system_top_options(*, session: Session) -> None:
    """Guarantee presence of system-wide top options for key metrics."""

    config_by_abbreviation = {
        config.abbreviation: config for config in FIELD_SERIES_CONFIGS
    }
    missing_configs = [
        abbreviation
        for abbreviation in KEY_METRIC_ABBREVIATIONS
        if abbreviation not in config_by_abbreviation
    ]
    if missing_configs:
        missing_list = ", ".join(sorted(missing_configs))
        raise RuntimeError(
            f"Не найдены конфигурации ключевых показателей: {missing_list}"
        )

    field_rows = session.execute(
        select(statistic_fields.c.abbreviation, statistic_fields.c.id)
        .where(statistic_fields.c.abbreviation.in_(KEY_METRIC_ABBREVIATIONS))
        .order_by(statistic_fields.c.abbreviation)
    ).mappings()
    field_ids = {row["abbreviation"]: row["id"] for row in field_rows}
    missing_fields = set(KEY_METRIC_ABBREVIATIONS) - field_ids.keys()
    if missing_fields:
        missing_list = ", ".join(sorted(missing_fields))
        raise RuntimeError(f"Не найдены поля статистики для топов: {missing_list}")

    existing_rows = session.execute(
        select(
            statistic_top_options.c.statistic_field_id,
            statistic_top_options.c.option_id,
            statistic_top_options.c.user_id,
        ).where(statistic_top_options.c.statistic_field_id.in_(field_ids.values()))
    ).mappings()
    existing_keys = {
        (
            row["statistic_field_id"],
            row["option_id"],
            row["user_id"],
        )
        for row in existing_rows
    }

    for abbreviation in KEY_METRIC_ABBREVIATIONS:
        field_id = field_ids[abbreviation]
        config = config_by_abbreviation[abbreviation]
        for template in SYSTEM_TOP_OPTION_TEMPLATES:
            key = (field_id, template.option_id, None)
            if key in existing_keys:
                continue
            session.execute(
                insert(statistic_top_options).values(
                    statistic_field_id=field_id,
                    entity_type=config.entity_type.value,
                    option_id=template.option_id,
                    label=template.label,
                    short_label=template.short_label,
                    order=template.order,
                    limit_value=template.limit_value,
                    value_from=template.value_from,
                    value_to=template.value_to,
                    user_id=None,
                )
            )
            existing_keys.add(key)


def load_statistic_filter_pool(*, session: Session) -> StatisticFilterPool:
    field_titles = (
        FILTER_FIELD_DEVICE_TYPE,
        FILTER_FIELD_TRAFFIC_SOURCE,
        FILTER_FIELD_COUNTRY_ID,
    )
    field_rows = session.execute(
        select(
            statistic_filter_fields.c.title,
            statistic_filter_fields.c.id,
        ).where(statistic_filter_fields.c.title.in_(field_titles))
    ).mappings()
    field_ids = {row["title"]: row["id"] for row in field_rows}
    missing_titles = set(field_titles) - set(field_ids)
    if missing_titles:
        missing_list = ", ".join(sorted(missing_titles))
        raise RuntimeError(f"Не найдены поля фильтров статистики: {missing_list}")

    device_titles = sorted({combo[0] for combo in FILTER_COMBINATIONS_FOR_DEMO})
    traffic_titles = sorted({combo[1] for combo in FILTER_COMBINATIONS_FOR_DEMO})

    device_rows = session.execute(
        select(
            statistic_filter_values.c.value,
            statistic_filter_values.c.id,
        )
        .where(
            statistic_filter_values.c.filter_field_id
            == field_ids[FILTER_FIELD_DEVICE_TYPE]
        )
        .where(statistic_filter_values.c.value.in_(device_titles))
    ).mappings()
    device_ids = {row["value"]: row["id"] for row in device_rows}
    missing_devices = set(device_titles) - set(device_ids)
    if missing_devices:
        missing_list = ", ".join(sorted(missing_devices))
        raise RuntimeError(
            f"Не найдены значения фильтра по типу устройства: {missing_list}"
        )

    traffic_rows = session.execute(
        select(
            statistic_filter_values.c.value,
            statistic_filter_values.c.id,
        )
        .where(
            statistic_filter_values.c.filter_field_id
            == field_ids[FILTER_FIELD_TRAFFIC_SOURCE]
        )
        .where(statistic_filter_values.c.value.in_(traffic_titles))
    ).mappings()
    traffic_ids = {row["value"]: row["id"] for row in traffic_rows}
    missing_traffic = set(traffic_titles) - set(traffic_ids)
    if missing_traffic:
        missing_list = ", ".join(sorted(missing_traffic))
        raise RuntimeError(
            f"Не найдены значения фильтра по источнику трафика: {missing_list}"
        )

    country_id = session.execute(
        select(statistic_filter_values.c.id)
        .where(
            statistic_filter_values.c.filter_field_id
            == field_ids[FILTER_FIELD_COUNTRY_ID]
        )
        .where(statistic_filter_values.c.value == COUNTRY_NAME_FOR_DEMO)
    ).scalar_one_or_none()
    if country_id is None:
        raise RuntimeError(f"Не найдено значение страны '{COUNTRY_NAME_FOR_DEMO}'")

    combinations = tuple(
        StatisticFilterCombination(
            device_type_id=device_ids[device_title],
            traffic_source_id=traffic_ids[traffic_title],
        )
        for device_title, traffic_title in FILTER_COMBINATIONS_FOR_DEMO
    )

    return StatisticFilterPool(
        combinations=combinations,
        country_id=country_id,
    )


def _compute_value(
    *,
    base: float,
    trend: float,
    noise: float,
    day_index: int,
    config: FieldSeriesConfig,
    rng: Random,
) -> float:
    raw_value = base + trend * day_index + rng.uniform(-noise, noise)
    if config.minimum is not None:
        raw_value = max(config.minimum, raw_value)
    if config.maximum is not None:
        raw_value = min(config.maximum, raw_value)
    return raw_value


def _format_value(*, value: float, config: FieldSeriesConfig) -> str:
    if config.expected_type is StatisticFieldType.integer:
        return str(int(round(value)))
    if config.decimals is None:
        return str(value)
    formatted = round(value, config.decimals)
    return f"{formatted:.{config.decimals}f}"


def create_statistic_values(
    *,
    session: Session,
    entity_records: Sequence[PageRecord | QueryRecord],
    configs: Sequence[FieldSeriesConfig],
    field_metadata: dict[str, FieldMetadata],
    entity_type: EntityTypeForStatistic,
    filter_pool: StatisticFilterPool,
    rng: Random,
    days: int = 5,
) -> None:
    """Generate multi-day statistic series for the provided entities."""

    dates = generate_recorded_dates(days=days)
    applicable_configs = [
        config for config in configs if config.entity_type is entity_type
    ]
    if not applicable_configs:
        return

    rows: list[dict[str, Any]] = []
    row_filters: list[tuple[UUID, UUID, UUID]] = []
    combinations = filter_pool.combinations
    if not combinations:
        raise RuntimeError(
            "Для генерации статистики требуется хотя бы одна комбинация фильтров"
        )

    for record_index, record in enumerate(entity_records):
        per_config_base: dict[str, float] = {}
        per_config_trend: dict[str, float] = {}
        for config in applicable_configs:
            per_config_base[config.abbreviation] = rng.uniform(*config.base_range)
            per_config_trend[config.abbreviation] = rng.uniform(*config.trend_range)

        combination = combinations[record_index % len(combinations)]
        for day_index, recorded_at in enumerate(dates):
            filter_values = (
                combination.device_type_id,
                combination.traffic_source_id,
                filter_pool.country_id,
            )
            for config in applicable_configs:
                metadata = field_metadata[config.abbreviation]
                base = per_config_base[config.abbreviation]
                trend = per_config_trend[config.abbreviation]
                value = _compute_value(
                    base=base,
                    trend=trend,
                    noise=config.noise,
                    day_index=day_index,
                    config=config,
                    rng=rng,
                )
                rows.append(
                    {
                        "entity_type": entity_type.value,
                        "entity_id": record.id,
                        "field_id": metadata.id,
                        "value": _format_value(value=value, config=config),
                        "recorded_at": recorded_at,
                    }
                )
                row_filters.append(filter_values)

    if rows:
        inserted_ids = (
            session.execute(
                insert(statistic_values).returning(statistic_values.c.id), rows
            )
            .scalars()
            .all()
        )
        link_rows: list[dict[str, Any]] = []
        for value_id, filters in zip(inserted_ids, row_filters, strict=True):
            for filter_value_id in filters:
                link_rows.append(
                    {
                        "statistic_value_id": value_id,
                        "filter_value_id": filter_value_id,
                    }
                )
        session.execute(insert(statistic_value_to_filter_values), link_rows)


def populate_demo_data() -> None:
    """Entrypoint that orchestrates demo data creation."""

    rng = Random(2024)
    security = Security()

    with SyncSession() as session:
        with session.begin():
            owner_id = ensure_demo_owner(session=session, security=security)
            clear_existing_demo_projects(
                session=session,
                project_names=[template.name for template in PROJECT_TEMPLATES],
            )

            field_metadata = load_field_metadata(
                session=session, configs=FIELD_SERIES_CONFIGS
            )
            ensure_system_top_options(session=session)
            filter_pool = load_statistic_filter_pool(session=session)

            for template in PROJECT_TEMPLATES:
                project_id = create_project(
                    session=session, template=template, owner_id=owner_id, rng=rng
                )
                pages_pool = create_pages_for_project(
                    session=session,
                    template=template,
                    project_id=project_id,
                    rng=rng,
                )
                clusters_pool = create_clusters_for_project(
                    session=session,
                    template=template,
                    project_id=project_id,
                    pages_pool=pages_pool,
                    rng=rng,
                )
                queries_pool = create_queries_for_project(
                    session=session,
                    template=template,
                    project_id=project_id,
                    clusters_pool=clusters_pool,
                    rng=rng,
                )
                create_statistic_values(
                    session=session,
                    entity_records=pages_pool,
                    configs=FIELD_SERIES_CONFIGS,
                    field_metadata=field_metadata,
                    entity_type=EntityTypeForStatistic.page,
                    filter_pool=filter_pool,
                    rng=rng,
                    days=5,
                )
                create_statistic_values(
                    session=session,
                    entity_records=queries_pool,
                    configs=FIELD_SERIES_CONFIGS,
                    field_metadata=field_metadata,
                    entity_type=EntityTypeForStatistic.query,
                    filter_pool=filter_pool,
                    rng=rng,
                    days=5,
                )
                print(
                    f"  • Страниц: {len(pages_pool)}, запросов: {len(queries_pool)}, кластеров: {len(clusters_pool)}"
                )

    print("Демо-данные успешно сгенерированы.")


if __name__ == "__main__":
    populate_demo_data()
