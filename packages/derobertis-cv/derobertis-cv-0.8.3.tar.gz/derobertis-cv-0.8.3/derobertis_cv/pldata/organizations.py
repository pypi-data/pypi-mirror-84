from derobertis_cv.models.organization import Organization
from derobertis_cv.pldata.cover_letters.models import ApplicationTarget, HiringManager, Gender

PLACEHOLDER_GOV = Organization(
    '(Government Organization name)',
    '(City, state)',
    abbreviation='(Government Organization abbreviation)',
    address_lines=[
        '(Organization division)',
        '(Street address)',
        '(City, state, ZIP)',
    ]
)

PLACEHOLDER_GOV_TARGET = ApplicationTarget(
    PLACEHOLDER_GOV,
    '(Position name)',
)

SEC_DERA = Organization(
    'U.S. Securities and Exchange Commission',
    'Washington, DC',
    abbreviation='DERA',
    address_lines=[
        'Division of Economic and Risk Analysis',
        '100 F Street, NE',
        'Washington, DC 20549',
    ]
)

WYNETTA_JONES = HiringManager(
    'Jones',
    first_name='Wynetta',
    gender=Gender.FEMALE,
    title='Lead HR Specialist',
)

DERA_COMMITTEE = HiringManager(
    'DERA Hiring Committee',
    is_person=False
)

SEC_DERA_TARGET = ApplicationTarget(
    SEC_DERA,
    'Financial Economic Fellow',
    person=DERA_COMMITTEE
)

OFR = Organization(
    'Office of Financial Research',
    'Washington, DC',
    abbreviation='OFR',
    address_lines=[
        'cover letter being sent as email',
    ]
)

OFR_TARGET = ApplicationTarget(
    OFR,
    'Research Economist',
)

RICH_FED = Organization(
    'Federal Reserve Bank of Richmond',
    'Charlotte, NC',
    abbreviation='QSR',
    address_lines=[
        'Quantitative Supervision & Research',
        '530 East Trade Street',
        'Charlotte, NC  28202',
    ]
)

RICH_FED_TARGET = ApplicationTarget(
    RICH_FED,
    'Financial Economist',
)

OCC_MARKET_RAD = Organization(
    'Office of the Comptroller of the Currency',
    'Washington, DC',
    abbreviation='OCC Market RAD',
    address_lines=[
        'Market Risk Analysis Division',
        '400 7th St. SW',
        'Washington, DC  20219'
    ]
)

OCC_MARKET_RAD_TARGET = ApplicationTarget(OCC_MARKET_RAD, 'Financial Economist')

OCC_CCRAD = Organization(
    'Office of the Comptroller of the Currency',
    'Washington, DC',
    abbreviation='OCC CCRAD',
    address_lines=[
        'Commercial Credit Risk Analysis Division',
        '400 7th St. SW',
        'Washington, DC  20219'
    ]
)

OCC_CCRAD_TARGET = ApplicationTarget(OCC_CCRAD, 'Financial Economist')

SEC_OIAD = Organization(
    'U.S. Securities and Exchange Commission',
    'Washington, DC',
    abbreviation='OIAD',
    address_lines=[
        'Office of the Investor Advocate',
        '100 F Street, NE',
        'Washington, DC 20549',
    ]
)

SEC_OIAD_TARGET = ApplicationTarget(SEC_OIAD, 'Financial Economist')

NY_FED = Organization(
    'Federal Reserve Bank of New York',
    'New York, NY',
    abbreviation='FRBNY',
    address_lines=[
        '33 Liberty Street',
        'New York, NY  10045',
    ]
)

NY_FED_TARGET = ApplicationTarget(
    NY_FED,
    'PhD Economist',
)


WORLD_BANK_DRG = Organization(
    'World Bank',
    'Washington, D.C.',
    abbreviation='DRG',
    address_lines=[
        'Development Research Group'
    ]
)

WORLD_BANK_DRG_HIRING = HiringManager(
    'DRG Hiring Committee',
    is_person=False
)

WORLD_BANK_DRG_TARGET = ApplicationTarget(WORLD_BANK_DRG, 'Researcher', person=WORLD_BANK_DRG_HIRING)

FED_BOARD = Organization(
    'Federal Reserve Board of Governors',
    'Washington, D.C.',
    abbreviation='the Board',
    address_lines=[
        '1850 K Street, NW',
        'Washington, D.C.  20006'
    ]
)

FED_BOARD_HIRING = HiringManager('Federal Reserve Board Hiring Committee', is_person=False)

FED_BOARD_TARGET = ApplicationTarget(FED_BOARD, 'Financial Economist', person=FED_BOARD_HIRING)

