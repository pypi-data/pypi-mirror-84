from derobertis_cv.models.organization import OrganizationCharacteristics
from derobertis_cv.models.university import UniversityModel
from derobertis_cv.pldata.constants.institutions import UF_NAME, VCU_NAME
from derobertis_cv.pldata.cover_letters.models import HiringManager, ApplicationTarget, Gender
from derobertis_cv.pltemplates.logo import image_base64

AP = 'Assistant Professor'

UF = UniversityModel(UF_NAME, 'Gainesville, FL', abbreviation='UF', logo_base64=image_base64('uf-logo.png'))
VCU = UniversityModel(VCU_NAME, 'Richmond, VA', abbreviation='VCU', logo_base64=image_base64('vcu-logo.png'))

PLACEHOLDER_UNIVERSITY = UniversityModel(
    '(School name)',
    '(City, state)',
    abbreviation='(School abbreviation)',
    address_lines=[
        '(Department name)',
        '(Street address)',
        '(City, state, ZIP)',
    ]
)

PLACEHOLDER_UNIVERSITY_TARGET = ApplicationTarget(
    PLACEHOLDER_UNIVERSITY,
    AP,
)

EL_PASO = UniversityModel(
    'University of Texas at El Paso',
    'El Paso, TX',
    abbreviation='UTEP',
    address_lines=[
        'Economics and Finance',
        'Business Room 236',
        '500 West University Avenue',
        'El Paso, TX  79968'
    ]
)

EL_PASO_TARGET = ApplicationTarget(
    EL_PASO,
    AP,
)

DRAKE = UniversityModel(
    'Drake University College of Business & Public Administration',
    'Des Moines, IA',
    abbreviation='DU',
    address_lines=[
        'Finance Department',
        'Aliber Hall',
        '2507 University Ave',
        'Des Moines, IA 50311',
    ]
)

DRAKE_TARGET = ApplicationTarget(
    DRAKE,
    AP,
)

MONASH = UniversityModel(
    'Monash University',
    'Melbourne, Victoria, Australia',
    abbreviation='MU',
    address_lines=[
        'Monash Business School',
        '900 Dandenong Road',
        'Caulfield East',
        'Victoria 3145',
        'Australia'
    ]
)

MONASH_HIRING_MANAGER = HiringManager(
    'Banking and Finance Recruitment Team',
    is_person=False
)

MONASH_TARGET = ApplicationTarget(
    MONASH,
    AP,
    person=MONASH_HIRING_MANAGER,
)

OREGON_STATE = UniversityModel(
    'Oregon State University',
    'Corvallis, OR',
    abbreviation='OSU',
    address_lines=[
        'College of Business',
        '2751 SW Jefferson Way',
        'Corvallis, OR  97331'
    ]
)

OREGON_STATE_TARGET = ApplicationTarget(
    OREGON_STATE,
    AP,
)

FIU = UniversityModel(
    'Florida International University',
    'Miami, FL',
    abbreviation='FIU',
    address_lines=[
        'College of Business',
        '11200 SW 8th St.',
        'Miami, FL  33174'
    ],
    city='Miami',
    characteristics=[
        OrganizationCharacteristics.WARM_WEATHER,
        OrganizationCharacteristics.LARGE_CITY,
    ]
)

FIU_TARGET = ApplicationTarget(FIU, AP)

UWM = UniversityModel(
    'University of Wisconsin Milwaukee',
    'Milwaukee, WI',
    abbreviation='UWM',
    address_lines=[
        'Sheldon B. Lubar School of Business',
        '3202 N Maryland Ave',
        'Milwaukee, WI  53202'
    ],
    city='Milwaukee',
    characteristics=[
        OrganizationCharacteristics.MID_SIZE_CITY,
    ]
)

UWM_TARGET = ApplicationTarget(UWM, AP)


QUEENS = UniversityModel(
    "Queen's University",
    'Kingston, ON, Canada',
    abbreviation='QU',
    address_lines=[
        'Smith School of Business',
        'Goodes Hall',
        '143 Union St.',
        'Kingston, Ontario',
        'Canada K7L 3N6'
    ],
    city='Kingston',
    country='Canada',
    characteristics=[
        OrganizationCharacteristics.MID_SIZE_CITY,
        OrganizationCharacteristics.INTERNATIONAL,
    ]
)

QUEENS_TARGET = ApplicationTarget(QUEENS, AP)

UMASS_BOSTON = UniversityModel(
    'University of Massachusetts Boston',
    'Boston, MA',
    abbreviation='UMass Boston',
    address_lines=[
        'Department of Accounting and Finance',
        '100 Morrissey Blvd.',
        'Boston, MA  02125-3393'
    ],
    city='Boston',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
    ]
)

UMASS_BOSTON_TARGET = ApplicationTarget(UMASS_BOSTON, AP)

CAL_STATE_FULLERTON = UniversityModel(
    'California State University, Fullerton',
    'Fullerton, CA',
    abbreviation='CSUF',
    address_lines=[
        'College of Business and Economics',
        '2550 Nutwood Ave.',
        'Fullerton, CA  92831'
    ],
    city='Fullerton',
    characteristics=[
        OrganizationCharacteristics.MID_SIZE_CITY,
        OrganizationCharacteristics.WEST_COAST,
        OrganizationCharacteristics.WARM_WEATHER
    ]
)

CAL_STATE_FULLERTON_TARGET = ApplicationTarget(CAL_STATE_FULLERTON, AP)

WILFRID_LAURIER = UniversityModel(
    'Wilfrid Laurier University',
    'Waterloo, ON, Canada',
    abbreviation='Laurier',
    address_lines=[
        'Associate Dean of Business: Faculty Development & Research',
        'Lazaridis School of Business & Economics',
        'Wilfrid Laurier University',
        'Waterloo, Ontario, N2L 3C5'
    ],
    city='Waterloo',
    country='Canada',
    characteristics=[
        OrganizationCharacteristics.MID_SIZE_CITY,
        OrganizationCharacteristics.INTERNATIONAL,
    ]
)

WILFRID_LAURIER_HM = HiringManager(
    'Mathieu',
    first_name='Robert',
    gender=Gender.MALE,
    title='Associate Dean of Business: Faculty Development & Research',
    is_doctor=True
)

WILFRID_LAURIER_TARGET = ApplicationTarget(WILFRID_LAURIER, AP + ' (2020-04)', person=WILFRID_LAURIER_HM)

U_TORONTO_SCARBOROUGH = UniversityModel(
    'University of Toronto Scarborough',
    'Scarborough, ON, Canada',
    abbreviation='UTSC',
    address_lines=[
        'Department of Management',
        '1265 Military Trail',
        'Scarborough, ON M1C 1A4',
    ],
    city='Toronto',
    country='Canada',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.INTERNATIONAL,
    ]
)

U_TORONTO_SCARBOROUGH_TARGET = ApplicationTarget(U_TORONTO_SCARBOROUGH, AP)

AMSTERDAM = UniversityModel(
    'University of Amsterdam',
    'Amsterdam, Netherlands',
    abbreviation='UvA',
    address_lines=[
        'Amsterdam Business School',
        'Plantage Muidergracht 12',
        '1018 TV Amsterdam, Netherlands'
    ],
    city='Amsterdam',
    country='Netherlands',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.INTERNATIONAL,
    ]
)

AMSTERDAM_TARGET = ApplicationTarget(AMSTERDAM, AP)

COPENHAGEN = UniversityModel(
    'Copenhagen Business School',
    'Frederiksberg, Denmark',
    abbreviation='CBS',
    address_lines=[
        'Solbjerg Plads 3',
        'DK-2000 Frederiksberg, Denmark'
    ],
    city='Frederiksberg',
    country='Denmark',
    characteristics=[
        OrganizationCharacteristics.MID_SIZE_CITY,
        OrganizationCharacteristics.INTERNATIONAL,
    ]
)

COPENHAGEN_TARGET = ApplicationTarget(COPENHAGEN, AP)

HEC_PARIS = UniversityModel(
    'HEC Paris',
    'Jouy-en-Josas, France',
    abbreviation='HEC',
    address_lines=[
        '1 Rue de la Libération',
        '78350 Jouy-en-Josas, France'
    ],
    city='Paris',
    country='France',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.INTERNATIONAL,
    ]
)

HEC_PARIS_TARGET = ApplicationTarget(HEC_PARIS, AP)

POMPEU_FABRA = UniversityModel(
    'Universitat Pompeu Fabra',
    'Barcelona, Spain',
    abbreviation='UPF',
    address_lines=[
        'Department of Economics and Business',
        'Edifici Jaume I (campus de la Ciutadella)',
        'Ramon Trias Fargas, 25-27',
        '08005 Barcelona'
    ],
    city='Barcelona',
    country='Spain',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.INTERNATIONAL,
        OrganizationCharacteristics.WARM_WEATHER,
    ]
)

POMPEU_FABRA_TARGET = ApplicationTarget(POMPEU_FABRA, AP)

EDHEC = UniversityModel(
    'EDHEC Business School',
    'Nice, France',
    abbreviation='EDHEC',
    address_lines=[
        '24 Avenue Gustave Delory',
        '59100 Roubaix, France'
    ],
    city='Nice',
    country='France',
    characteristics=[
        OrganizationCharacteristics.MID_SIZE_CITY,
        OrganizationCharacteristics.INTERNATIONAL,
    ]
)

EDHEC_TARGET = ApplicationTarget(EDHEC, AP)

BOCCONI = UniversityModel(
    'Bocconi University',
    'Milan, Italy',
    abbreviation='Bocconi',
    address_lines=[
        'Via Roberto Sarfatti',
        '25, 20100 Milano MI',
        'Italy',
    ],
    city='Milan',
    country='Italy',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.INTERNATIONAL,
    ]
)

BOCCONI_TARGET = ApplicationTarget(BOCCONI, AP)
