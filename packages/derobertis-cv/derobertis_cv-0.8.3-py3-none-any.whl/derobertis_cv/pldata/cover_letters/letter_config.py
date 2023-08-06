from typing import List, Sequence

import pyexlatex as pl

from derobertis_cv.pldata.authors import AUTHORS
from derobertis_cv.pldata.constants.authors import NIMAL, ANDY
from derobertis_cv.pldata.cover_letters.models import CoverLetter, ApplicationComponents, ApplicationFocus, \
    CoverLetterDesireSection
from derobertis_cv.pldata.organizations import SEC_DERA_TARGET, OFR_TARGET, RICH_FED_TARGET, PLACEHOLDER_GOV_TARGET
import derobertis_cv.pldata.organizations as orgs
from derobertis_cv.pldata.universities import EL_PASO_TARGET, DRAKE_TARGET, PLACEHOLDER_UNIVERSITY_TARGET, \
    MONASH_TARGET, OREGON_STATE_TARGET, FIU_TARGET, UWM_TARGET
import derobertis_cv.pldata.universities as univs


def get_cover_letters() -> List[CoverLetter]:
    exclude_components: Sequence[ApplicationComponents] = (
        ApplicationComponents.OTHER_RESEARCH,
        ApplicationComponents.EMAIL_BODY,
        ApplicationComponents.COVER_LETTER_AS_EMAIL,
        ApplicationComponents.ALL,
        ApplicationComponents.REFERENCES,
        ApplicationComponents.COVER_LETTER,
        ApplicationComponents.INVESTOR_ATTENTION_PAPER,
        ApplicationComponents.PERSONAL_WEBSITE,
    )
    all_concrete_components = [comp for comp in ApplicationComponents if comp not in exclude_components]

    exclude_government_components: Sequence[ApplicationComponents] = (
        *exclude_components,
        ApplicationComponents.TEACHING_STATEMENT,
        ApplicationComponents.DIVERSITY,
        ApplicationComponents.EVALUATIONS,
        ApplicationComponents.COURSE_OUTLINES,
    )

    all_government_components = [
        comp for comp in ApplicationComponents if comp not in exclude_government_components
    ]

    all_government_components_no_transcripts = [
        comp for comp in ApplicationComponents
        if comp not in (*exclude_government_components, ApplicationComponents.TRANSCRIPTS)
    ]

    exclude_industry_components: Sequence[ApplicationComponents] = (
        *exclude_government_components,
        ApplicationComponents.TRANSCRIPTS,
        ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
        ApplicationComponents.OPIN_PAPER,
        ApplicationComponents.RESEARCH_STATEMENT,
    )

    all_industry_components = [
        comp for comp in ApplicationComponents if comp not in exclude_industry_components
    ]

    courses_site_footnote = pl.Footnote(
        f'See all the course topics on the {CoverLetter.site_link("courses page", "courses")} of my personal website.'
    )

    return [
        CoverLetter(
            PLACEHOLDER_GOV_TARGET,
            [
"""
(Organization-specific paragraph)
""",
            ],
            included_components=all_concrete_components,
            focus=ApplicationFocus.GOVERNMENT,
        ),
        CoverLetter(
            PLACEHOLDER_UNIVERSITY_TARGET,
            [
                """
                (School-specific paragraph)
                """,
            ],
            included_components=all_concrete_components,
            focus=ApplicationFocus.ACADEMIC,
        ),
        CoverLetter(
            SEC_DERA_TARGET,
            [
"""
I believe I am an ideal fit at DERA as a Financial Economic Fellow given my related research in valuation,
corporate finance, and economic policy as well as technical skills related to developing economic models and
communicating insights from large quantities of data. I have a strong interest in regulatory issues in financial
markets and am equally comfortable being both self-guided and a team player providing high-quality results and
recommendations. Further, I have a locational preference towards Washington, DC as my family lives in
Northern Virginia, though I would be pleased to work at any potential DERA location.
""",
            ],
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.TRANSCRIPTS,
                ApplicationComponents.JOB_MARKET_PAPER
            ],
            focus=ApplicationFocus.GOVERNMENT,
            included_references=(AUTHORS[ANDY], AUTHORS[NIMAL]),
            font_scale=0.93
        ),
        CoverLetter(
            EL_PASO_TARGET,
            [
"""
I believe I am an ideal fit at UTEP given that you are looking for an applicant in the area of investments and 
corporate finance, and I have research work in both. Further, the posting mentions FinTech under the preferred
specialties, and my Financial Modeling course is geared towards preparation for FinTech roles considering it 
combines finance knowledge and programming. On a personal level, my wife and I both have an affinity for 
mid-size cities and warm weather.
"""
            ],
            included_components=[
                ApplicationComponents.CV,
            ],
            focus=ApplicationFocus.ACADEMIC,
        ),
        CoverLetter(
            DRAKE_TARGET,
            [
"""
I believe I am an ideal fit at DU given that you are looking for an applicant who can teach corporate finance, 
valuation, and FinTech, and my Financial Modeling course hits on all these topics. I teach programming and 
modeling skills that prepare students for FinTech roles, and the projects in the course are related to 
DCF valuation and capital budgeting. Further, most of my research work involves valuation and my job market
paper is in the FinTech area due to the topic of cryptocurrencies. On a personal level, my wife and I both 
have an affinity for mid-size cities and outdoor activities so I think we would feel right at home in Des Moines.
"""
            ],
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.DIVERSITY,
                ApplicationComponents.TRANSCRIPTS,
                ApplicationComponents.EVALUATIONS,
            ],
            focus=ApplicationFocus.ACADEMIC,
        ),
        CoverLetter(
            OFR_TARGET,
            [
"""
I believe I am an ideal fit at OFR as a Research Economist given my related research in market microstructure and 
macroeconomics, as well as technical skills related to developing economic models and
communicating insights from large quantities of data. I have a strong interest in regulatory issues in financial
markets and am equally comfortable being both self-guided and a team player providing high-quality results and
recommendations. Further, I have a locational preference towards Washington, DC as my family lives in
Northern Virginia. Should I be selected, I would like to start at the end of July or beginning of August, but
I can be flexible on the timing.
"""
            ],
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER
            ],
            focus=ApplicationFocus.GOVERNMENT,
            as_email=True
        ),
        CoverLetter(
            RICH_FED_TARGET,
            [
"""
I believe I am an ideal fit at the Richmond Fed as a Financial Economist given my related research in market microstructure, 
macroeconomics, and economic policy as well as technical skills related to developing economic models and
communicating insights from large quantities of data. I am familiar with the Fed's supervisory work from both ends: 
I was an intern in the Credit Risk department at the Board of Governors and I worked directly with examiners in my 
role as a Portfolio Analyst rebuilding the models for the Allowance for Loan and Lease Losses at 
Eastern Virginia Bankshares. 
I have a strong interest in regulatory issues in financial
markets and am equally comfortable being both self-guided and a team player providing high-quality results and
recommendations. On a personal level, my wife and I both 
have an affinity for larger cities and my family is in Virginia so Charlotte and Baltimore would both be 
great locations for us.
"""
            ],
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.INVESTOR_ATTENTION_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
            ],
            focus=ApplicationFocus.GOVERNMENT,
            font_scale=0.95,
            line_spacing=0.8,
        ),
        CoverLetter(
            MONASH_TARGET,
            [
"""
I believe I am an ideal fit at MU given that you are looking for an applicant with research and 
teaching experience in complex financial instruments, financial modeling, and international
finance. As my job market paper develops a model of cryptocurrency valuation and tests it empirically,
it is related to the first two of those areas. The Government Equity Capital Market Intervention study analyzes 
the effects of the Bank of Japan intervening in equity markets through
ETF purchases so it is related to the third. Finally, by the time I would start I will have two years 
of experience teaching my Financial Modeling course. On a personal level, my wife and I have been interested 
in living abroad and would like to be in a larger city with warm weather so Melbourne seems like a great fit.
"""
            ],
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
            ],
            focus=ApplicationFocus.ACADEMIC,
            line_spacing=1.1,
            by_email=True,
        ),
        CoverLetter(
            OREGON_STATE_TARGET,
            [
"""
My multiple lines of research and strong work ethic will contribute to the College of Business' goal of preeminence in 
research. Further, I will contribute to the goals of innovation and transformative, accessible education. 
It may already be apparent that I am not the typical Finance Ph.D. applicant: I have a much
larger emphasis on creating open-source software. My commitment to open-source is a commitment to inclusion and 
diversity: I believe everyone should have access to these tools regardless of their economic position, 
and that anyone should be able to learn from them, regardless of their location in the world or cultural 
background. I have already built tools for both research and education, and I want to continue innovating
at a university that encourages such efforts. On a personal level, my wife and I have always wanted to move to the 
West Coast and we enjoy outdoor activities so Corvallis seems like a good fit.
"""
            ],
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.TEACHING_STATEMENT,
                ApplicationComponents.RESEARCH_STATEMENT,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.EVALUATIONS
            ],
            focus=ApplicationFocus.ACADEMIC,
            file_renames={
                ApplicationComponents.JOB_MARKET_PAPER: 'Job Market Paper',
            }
        ),
        CoverLetter(
            FIU_TARGET,
            CoverLetterDesireSection(FIU_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.TRANSCRIPTS,
                ApplicationComponents.EVALUATIONS,
                ApplicationComponents.RESEARCH_STATEMENT,
                ApplicationComponents.TEACHING_STATEMENT,
            ],
            focus=ApplicationFocus.ACADEMIC,
            line_spacing=1.1,
            font_scale=1.05,
        ),
        CoverLetter(
            UWM_TARGET,
            CoverLetterDesireSection(UWM_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.REFERENCES,
            ],
            focus=ApplicationFocus.ACADEMIC,
            line_spacing=1.1,
            font_scale=1.05,
        ),
        CoverLetter(
            univs.QUEENS_TARGET,
            CoverLetterDesireSection(univs.QUEENS_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.TEACHING_STATEMENT,
                ApplicationComponents.COURSE_OUTLINES,
                ApplicationComponents.EVALUATIONS,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
            ],
            focus=ApplicationFocus.ACADEMIC
        ),
        CoverLetter(
            univs.UMASS_BOSTON_TARGET,
            [
"""
I believe I am an ideal fit at UMass Boston as you are looking for an applicant in the field of 
financial technology. I have applied machine learning and textual analysis in my research,  
my job market paper is focused on cryptoassets, I am currently researching the broader decentralized 
finance space, and I have deep expertise in programming and 
data science. You are also looking for someone to teach Ph.D. students this kind of material,
and beyond my multiple full undergraduate courses, I have given numerous informal seminars to fellow
Ph.D students on programming topics such as web-scraping, automation, Python for research applications, 
and machine learning,
and I am widely viewed in the department as a resource on such topics. I also very much enjoy teaching Ph.D. students
as we can cover much more material and it is more likely to lead to research ideas and collaboration. On a personal 
level, my wife and I have an affinity for larger cities and we already have family near Boston so it seems 
like a good fit.
""",
            ],
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.EVALUATIONS,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
            ],
            focus=ApplicationFocus.ACADEMIC
        ),
        CoverLetter(
            univs.CAL_STATE_FULLERTON_TARGET,
f"""
I believe I am an ideal fit at CSUF as you are looking for an applicant in the field of investments.
Nearly all of my research work is focused on investments whether it be stocks, options, or cryptoassets. 
Further, both of the courses I've developed and taught, Debt and Money Markets and Financial Modeling,
have substantial portions devoted to investment-related topics.{courses_site_footnote}
On a personal level, my wife and I have an affinity for mid-side
cities, the West Coast, and warm weather so Fullerton seems like a good fit.
""",
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.RESEARCH_STATEMENT,
                ApplicationComponents.TEACHING_STATEMENT,
                ApplicationComponents.TRANSCRIPTS,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.DIVERSITY,
            ],
            focus=ApplicationFocus.ACADEMIC,
            combine_files={
                'Nick DeRobertis Research Works': [
                    ApplicationComponents.JOB_MARKET_PAPER,
                    ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                    ApplicationComponents.OPIN_PAPER,
                ]
            },
            file_renames={
                ApplicationComponents.CV: 'Nick DeRobertis CV',
                ApplicationComponents.DIVERSITY: 'Nick DeRobertis Statement on Commitment to Inclusive Excellence'
            }
        ),
        CoverLetter(
            univs.WILFRID_LAURIER_TARGET,
            CoverLetterDesireSection(univs.WILFRID_LAURIER_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
            ],
            focus=ApplicationFocus.ACADEMIC,
            by_email=True,
            add_organization_name_to_address=False,
            file_renames={
                ApplicationComponents.CV: 'Nick DeRobertis CV',
                ApplicationComponents.COVER_LETTER: 'Nick DeRobertis Cover Letter AP Finance 2020-04'
            }
        ),
        CoverLetter(
            orgs.OCC_MARKET_RAD_TARGET,
            [
"""
I believe I am an ideal fit at OCC Market RAD as a Financial Economist given my related research in asset pricing,
market microstructure, 
macroeconomics, and economic policy as well as technical skills related to developing economic models and
communicating insights from large quantities of data. I am familiar with banking supervisory work from both ends: 
I was an intern in the Credit Risk department at the Federal Reserve Board of Governors and 
I worked directly with examiners in my 
role as a Portfolio Analyst rebuilding the models for the Allowance for Loan and Lease Losses and developing 
a stress testing program at 
Eastern Virginia Bankshares. 
I have a strong interest in regulatory issues in financial
markets and am equally comfortable being both self-guided and a team player providing high-quality results and
recommendations. I am a U.S. citizen so I look forward to serving my country in this capacity.
On a personal level, my wife and I both 
have an affinity for larger cities and my family is in Northern Virginia so DC would be a 
great location for us.
"""
            ],
            included_components=all_government_components_no_transcripts,
            focus=ApplicationFocus.GOVERNMENT,
            as_email=True
        ),
        CoverLetter(
            orgs.OCC_CCRAD_TARGET,
            [
"""
I believe I am an ideal fit at OCC CCRAD as a Financial Economist given my related research in asset pricing,
market microstructure, 
macroeconomics, and economic policy as well as technical skills related to developing economic models and
communicating insights from large quantities of data. I am familiar with banking supervisory work from both ends: 
I was an intern in the Credit Risk department at the Federal Reserve Board of Governors and 
I worked directly with examiners in my 
role as a Portfolio Analyst rebuilding the models for the Allowance for Loan and Lease Losses and developing 
a stress testing program at 
Eastern Virginia Bankshares. 
I have a strong interest in regulatory issues in financial
markets and am equally comfortable being both self-guided and a team player providing high-quality results and
recommendations. I am a U.S. citizen so I look forward to serving my country in this capacity.
On a personal level, my wife and I both 
have an affinity for larger cities and my family is in Northern Virginia so DC would be a 
great location for us.
"""
            ],
            included_components=all_government_components_no_transcripts,
            focus=ApplicationFocus.GOVERNMENT,
            as_email=True
        ),
        CoverLetter(
            orgs.SEC_OIAD_TARGET,
            [
"""
I believe I am an ideal fit at OIAD as a Financial Economic Fellow given my related research in behavioral finance,
asset pricing, and corporate finance, as well as technical skills related to developing economic models and
communicating insights from large quantities of data. I have a strong interest in regulatory issues in financial
markets and am equally comfortable being both self-guided and a team player providing high-quality results and
recommendations. On a personal level, my wife and I both 
have an affinity for larger cities and my family is in Northern Virginia so DC would be a 
great location for us.
""",
            ],
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER
            ],
            focus=ApplicationFocus.GOVERNMENT,
            font_scale=0.93,
            by_email=True
        ),
        CoverLetter(
            univs.U_TORONTO_SCARBOROUGH_TARGET,
            CoverLetterDesireSection(univs.U_TORONTO_SCARBOROUGH_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.RESEARCH_STATEMENT,
                ApplicationComponents.TEACHING_STATEMENT,
                ApplicationComponents.COURSE_OUTLINES,
                ApplicationComponents.EVALUATIONS,
            ],
            focus=ApplicationFocus.ACADEMIC,
            combine_files={
                'Nick DeRobertis Application Package': [
                    ApplicationComponents.RESEARCH_STATEMENT,
                    ApplicationComponents.JOB_MARKET_PAPER,
                    ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                    ApplicationComponents.OPIN_PAPER,
                    ApplicationComponents.TEACHING_STATEMENT,
                    ApplicationComponents.COURSE_OUTLINES,
                    ApplicationComponents.EVALUATIONS,
                ]
            },
            output_compression_level=1
        ),
        CoverLetter(
            univs.AMSTERDAM_TARGET,
            CoverLetterDesireSection(univs.AMSTERDAM_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
            ],
            focus=ApplicationFocus.ACADEMIC,
            as_email=True,
        ),
        CoverLetter(
            orgs.NY_FED_TARGET,
            [
"""
I believe I am an ideal fit at FRBNY as a Financial Economist given my related research in market microstructure, 
macroeconomics, and economic policy as well as technical skills related to developing economic models and
communicating insights from large quantities of data. I am familiar with the Fed's supervisory work from both ends: 
I was an intern in the Credit Risk department at the Board of Governors and I worked directly with examiners in my 
role as a Portfolio Analyst rebuilding the models for the Allowance for Loan and Lease Losses at 
Eastern Virginia Bankshares. 
I have a strong interest in regulatory issues in financial
markets and am equally comfortable being both self-guided and a team player providing high-quality results and
recommendations. On a personal level, my wife and I both 
have an affinity for large cities and have family near New York so it would be a 
great location for us.
"""
            ],
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.TRANSCRIPTS,
            ],
            focus=ApplicationFocus.GOVERNMENT,
            font_scale=0.95,
            line_spacing=0.8,
            output_compression_level=1,
        ),
        CoverLetter(
            univs.COPENHAGEN_TARGET,
            CoverLetterDesireSection(univs.COPENHAGEN_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.RESEARCH_STATEMENT,
                ApplicationComponents.TEACHING_STATEMENT,
                ApplicationComponents.EVALUATIONS,
                ApplicationComponents.REFERENCES,
            ],
            focus=ApplicationFocus.ACADEMIC,
        ),
        CoverLetter(
            univs.HEC_PARIS_TARGET,
            CoverLetterDesireSection(univs.HEC_PARIS_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
            ],
            focus=ApplicationFocus.ACADEMIC,
        ),
        CoverLetter(
            univs.POMPEU_FABRA_TARGET,
            CoverLetterDesireSection(univs.POMPEU_FABRA_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.TRANSCRIPTS,
            ],
            focus=ApplicationFocus.ACADEMIC,
            combine_files={
                'Nick DeRobertis UPF Cover Letter and Transcripts': [
                    ApplicationComponents.COVER_LETTER,
                    ApplicationComponents.TRANSCRIPTS,
                ]
            }
        ),
        CoverLetter(
            orgs.WORLD_BANK_DRG_TARGET,
            [
"""
I believe I am an ideal fit at DRG as a Researcher given my related research in macroeconomics, 
economic policy,
market microstructure, and corporate finance, 
as well as technical skills related to developing economic models and
communicating insights from large quantities of data. I have a strong interest in development issues
and am equally comfortable being both self-guided and a team player providing high-quality results and
recommendations.
On a personal level, my wife and I both 
have an affinity for larger cities and my family is in Northern Virginia so DC would be a 
great location for us.
"""
            ],
            included_components=[
                ApplicationComponents.PERSONAL_WEBSITE,
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
            ],
            focus=ApplicationFocus.GOVERNMENT,
        ),
        CoverLetter(
            univs.EDHEC_TARGET,
            [
"""
I believe I am an ideal fit at EDHEC as you are looking for an applicant willing to teach 
Mathematical Finance or Machine Learning for Finance. I have applied machine learning and textual analysis in my research,  
I do some theory work, and I have deep expertise in programming and 
data science. Beyond my multiple full undergraduate courses, I have given numerous informal seminars to fellow
Ph.D students on programming topics such as machine learning and Python for research applications, 
and I am widely viewed in the department as a resource on such topics. I believe the industry is headed 
more towards quantitative finance, machine learning, and big data, and I would be excited at the opportunity 
to teach students these skills. On a personal level, my wife and I have an affinity for larger
cities, and have been hoping for an opportunity to live abroad from the US, so Paris and France seem like
a good fit.
"""
            ],
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.REFERENCES,
            ],
            included_references=[AUTHORS[ANDY], AUTHORS[NIMAL]],
            focus=ApplicationFocus.ACADEMIC,
            by_email=True
        ),
        CoverLetter(
            orgs.FED_BOARD_TARGET,
            [
"""
I believe I am an ideal fit at the Board as a Financial Economist given my related research in market microstructure, 
macroeconomics, and economic policy as well as technical skills related to developing economic models and
communicating insights from large quantities of data. I am familiar with the Fed's supervisory work from both ends: 
I was an intern in the Credit Risk department at the Board and I worked directly with examiners in my 
role as a Portfolio Analyst rebuilding the models for the Allowance for Loan and Lease Losses at 
Eastern Virginia Bankshares. 
I have a strong interest in regulatory issues in financial
markets and am equally comfortable being both self-guided and a team player providing high-quality results and
recommendations. On a personal level, my wife and I both 
have an affinity for larger cities and my family is in Northern Virginia so DC would be a 
great location for us.
"""
            ],
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.DIVERSITY,
            ],
            focus=ApplicationFocus.GOVERNMENT,
            font_scale=0.95,
            line_spacing=0.8,
        ),
        CoverLetter(
            univs.BOCCONI_TARGET,
"""
I believe I am an ideal fit at Bocconi as you are looking for an applicant in the fields of 
Financial Markets, Financial Institutions, Corporate Finance, and Mathematical Finance. 
My research touches on all of these components: all of my research is related to financial markets,
my Government Intervention paper focuses on financial institutions and several of my works in progress 
are related to corporate finance.
As far as Mathematical Finance, I have applied machine learning and textual analysis in my research,  
I do some theory work, and I have deep expertise in programming and 
data science. Beyond my multiple full undergraduate courses, I have given numerous informal seminars to fellow
Ph.D students on programming topics such as machine learning and Python for research applications, 
and I am widely viewed in the department as a resource on such topics. On a personal level, my wife 
and I have an affinity for larger
cities, have been hoping for an opportunity to live abroad from the US, and much of my ancestry is Italian
so Milan and Italy seem like a good fit.
""",
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.JMP_VIDEO
            ],
            focus=ApplicationFocus.ACADEMIC,
            video_output_format='mp4',
            video_desired_size_mb=5,
            combine_files={
                'Cover Letter and Other Research Work': [
                    ApplicationComponents.COVER_LETTER,
                    ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                    ApplicationComponents.OPIN_PAPER,
                ]
            },
            output_compression_level=1,
        ),
    ]
