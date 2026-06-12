ANNEX II Key messages to be sent by the economic operators

The messages required for regulatory purposes shall contain at least the data fields listed in this Annex. Both the ID issuer and the provider of the data repository (including the router) may decide to extend the message content for strictly technical purposes to secure smooth functioning of the tobacco products traceability system.

The messages listed in this Annex do not include the messages to be sent back by the ID issuer and the provider of the data repository (including the router) to the economic operators, such as acknowledgments of receipt.

All the messages generated within the tobacco traceability system shall contain the identification of the originator and a timestamp up to the second (see Data Type: Time(L)). This timestamp does not replace the time of the occurrence of a reported event, which shall be reported separately in accordance with the data fields prescribed in this Annex. The identification of the message originator, which may concern a third-party IT service provider, does not replace the identification of the economic operator responsible for the reporting activity (via an EOID to be indicated in the EO_ID field) The means of the identification of the message originator shall be specified in the technical specifications established and updated in accordance with Article 28.

The ID issuer and the provider of the data repository (including the router) shall timestamp each received message up to the millisecond.

CHAPTER I FIELD DESCRIPTIONS

SECTION 1 Data Type

Data Type Description Example

ARC

Administrative Reference Code (ARC) or any successive code adopted under the Excise  Movement and Control System (EMCS)

‘15GB0123456789A BCDEF0 ’ aUI

Aggregated level unique identifier coded with: either the invariant set of ISO646:1991 and composed of four blocks: (a) ID issuer's prefix in accordance with ISO15459-2:2015, (b) serialisation element in the format established by the ID issuer, (c) tobacco facility identifier code following the Data Type: FID and (d) timestamp following the Data Type: Time(s) or the invariant set of ISO646:1991 forming a code structured in accordance with ISO15459-1:2014 or ISO15459-4:2014 (or their latest equivalent)

Boolean

Boolean value

‘0’ (false/disabled) ‘1’ (true/enabled)

Country

Country name coded with ISO-3166-1:2013 alpha-2 (or its latest equivalent)

‘GI’

Currency

Currency name coded with ISO 4217:2015 (or its latest equivalent)

‘GIP’

Date

UTC (Coordinated Universal Time) date corresponding to the following format: YYYY- MM-DD

‘2019-05-20’

Decimal

Number values, decimal allowed

‘1’ or ‘2,2’ or ‘3,33’

EOID

Economic operator identifier code corresponding to the format established by the ID issuer coded with the invariant set of ISO646:1991

FID

Tobacco facility identifier code corresponding to the format established by the ID issuer coded with the invariant set of ISO646:1991

Integer

Rounded number values, no decimal numbers

‘1’ or ‘22’ or ‘333’

MID

Machine identifier code corresponding to the format established by the ID issuer coded with the invariant set of ISO646:1991

MRN

Movement Reference Number (MRN) is a unique customs registration number. It contains 18 digits and is composed of  the  following elements:  (a)  last two digits of the year of formal acceptance of export movement (YY), (b) where a declaration was sent to Gibraltar, the Gibraltar country name  coded with ISO-3166-1:2013 alpha-2 (or its latest equivalent), (c) unique identifier for entry/import per year and country, and (d) check digit.

‘11IT9876AB88901 235’

SEED

Excise number composed of: (a) country name coded with ISO-3166- 1:2013 alpha-2 (or its latest equivalent) (e.g. ‘LU’) and (b) eleven alphanumeric characters, if needed, padded to the left with zeroes (e.g. ‘00000987ABC’).

‘LU00000987ABC’

ITU

Individual transport unit code (e.g. SSCC) generated in accordance with ISO15459-1:2014 (or its latest equivalent)

‘0012345600000000 18 ’

Text

Set of characters coded with ISO8859-15:1999

‘Abcde12345’

Time(L)

UTC (Coordinated Universal Time) in the following format: YYYY- MM-DDTHH:mm:ss.SSSZ

‘2019-07- 16T19:20:30.205Z’

Time(s)

UTC (Coordinated Universal Time) in the following format: YYMMDDhh

‘19071619’

TPID

Tobacco Product Identifier (TP-ID) – numeric identifier used in the CEG system  in  the format: NNNNN-NN-NNNNN

‘02565-16-00230’

PN

Product number – numeric identifier used in the CEG system to identify product presentations (e.g. GTIN (Global Trade  Identification  Number) of the product)

‘00012345600012’

upUI(L)

Unit packet level unique identifier coded with the invariant set of ISO646:1991 and composed of three blocks: (a) ID Issuer's prefix in accordance with ISO15459-2:2015, (b) middle block in the format established by the ID issuer and (c) timestamp following the Data Type: Time(s) upUI(i) Unit packet level unique identifier coded with the invariant set of ISO646:1991 and composed of two blocks: (i) ID issuer’s prefix in accordance with ISO15459-2:2015 and (ii) middle block in the format established by the ID issuer (i.e. upUI(i) is upUI(L) without the timestamp, a code to be generated by ID issuers in accordance with Article 8(2) of this Regulation

upUI(s)

Unit packet level unique identifier coded with the invariant set of ISO646:1991 and composed of two blocks: (a) ID issuer's prefix in accordance with ISO15459-2:2015 and (b) serialisation element in the format established by the ID issuer (i.e. UI made visible in the human readable format on the unit packets)

upUI(M) Unit packet level unique identifier coded with the invariant set of ISO646:1991 and composed of 2 blocks: ID issuer’s prefix in accordance with ISO 154592:2015, middle block in the format established by the ID issuer LECNIzzzz0000100 00SLE

Year

UTC (Coordinated Universal Time) year in the following format: YYYY

‘2024’

SECTION 2 Cardinality Type

Type Description

Simple (S)

Single value

Multiple (M)

Multiple values

SECTION 3 Priority Type

Type Description

Mandatory (M)

The variable must be completed to successfully submit the message

Optional (O)

The variable relates to supplementary fields which remain optional

CHAPTER II

MESSAGES

SECTION 1

Identifier codes for economic operators, facilities and machines 1.1 Request for an economic operator identifier code

Item #

Field

Comments

Data Type

Cardinali ty

Priority

Values

Message_Type

Identification of message type

Text

S

M

1-1

EO_Name1

Economic operator's registered name

Text

S

M

EO_Name2

Economic operator's alternative or abridged name

Text

S

O

EO_street Economic opertor’s street name and house number (or road number and kilometre) Text S M

EO_municipali ty Economic operator’s municipality (city, town or village) Text S M

EO_postcode Economic operator’s postal code Text S M ‘n/a’ is permitted value if no postal code has been assigned

EO_A_info

Additional information on economic operator’s address (e.g. location in the shopping mall or industrial area)

Text

S

O

EO_Country- Reg

Economic operator's country of registration

Country

S

M

EO_Email

Economic operator's email address used to inform about registration process, including subsequent changes and other required correspondence

Text

S

M

VAT_R

Indication of the VAT registration status

Boolean

S

M

0 – No VAT registration 1 – VAT number exists

VAT_N

Economic operator's VAT number

Text

S

M, if VAT_R= 1

TAX_N

Economic operator's tax regis- tration number

Text

S

M, if VAT_R= 0

EO_Excise- Number1

Indication if the economic operator has an excise number issued by  the  competent authority for the purpose of identification of persons/premises

Boolean

S

M

0– No SEED number 1– SEED number exists

EO_Excise- Number2

Economic operator's excise number issued by the competent authority for the purpose of identification of persons/premises

SEED

S

M, if EO_ ExciseNumber 1= 1

Reg_3RD

Indication if the registration is made on behalf of a retail outlet operator not involved otherwise in the tobacco trade

Boolean

S

M

0 – No 1– Yes

Reg_EOID

Identifier of the  economic operator that acts on behalf of a retail outlet operator not involved otherwise in the tobacco trade

EOID

S

M, if Reg_ 3RD = 1

1.2 Correction of information concerning the economic operator identifier code

Item #

Field

Comments

Data Type Cardinality Priority

Values

Message_Type

Identification of message type

Text

S

M

1-2

EO_ID

Economic operator identifier code

EOID

S

M

EO_CODE

Economic operator's confirmation code provided in response to the registration of economic operator

Text

S

M

EO_Name1

Economic operator's registered name

Text

S

M

EO_Name2

Economic operator's alternative or abridged name

Text

S

O

EO_street Economic opertor’s street name and house number (or road number and kilometre) Text S M

EO_municipali ty Economic operator’s municipality (city, town or village) Text S M

EO_postcode Economic operator’s postal code Text S M ‘n/a’ is permitted value if no postal code has been assigned

EO_A_info

Additional information on economic operator’s address (e.g. location in the shopping mall or industrial area)

Text

S

O

EO_CountryR- eg

Economic operator's country of registration

Country

S

M

EO_Email

Economic operator's email address used to inform about registration process, including subsequent changes

Text

S

M

VAT_R

Indication of the VAT registration status

Boolean

S

M

0 – No VAT registration 1 – VAT number exists

VAT_N

Economic operator's VAT number

Text

S

M, if VAT_R= 1

TAX_N

Economic operator's tax registration number -

Text

S

M, if VAT_R = 0

EO_Excise- Number1

Indication if the economic operator has an excise number issued by the competent authority for the purpose of identification of persons/premises

Boolean

S

M

0 - No SEED number

1 - SEED number exists

EO_Excise- Number2

Economic operator's excise number issued by the competent authority for the purpose of identification of persons/premises

SEED

S

M, if EO_ Excise Number1= 1

OtherEOID_R

Indication if the economic operator has been allocated an identifier by another ID Issuer

Boolean

S

M

0 – No

1 - Yes

OtherEOID_N

Economic operator identifier codes allocated by other ID Issuers

EOID

M

M, if OtherEOID _R = 1

Reg_3RD

Indication if the registration is made on behalf of  the retail outlet operator not involved otherwise in the tobacco trade

Boolean

S

M

0 - No

1 - Yes

Reg_EOID

Identifier of the  economic operator that acts on behalf of the retail outlet operator not involved otherwise in the tobacco trade

EOID

S

M, if Reg_3RD = 1

1.3 De-registration of economic operator identifier code

Item #

Field

Comments

Data Type Cardinality Priority

Values

Message_Type

Identification of message type

Text

S

M

1-3

EO_ID

Economic operator identifier code

EOID

S

M

EO_CODE

Economic operator's confirmation code provided in response to the registration of economic operator

Text

S

M

Reg_3RD

Indication if the registration is made on behalf of  the  retail outlet operator not involved otherwise in the tobacco trade

Boolean

S

M

0 - No 1 - Yes

Reg_EOID

Identifier of the economic operator that acts on behalf of the retail outlet operator not involved  otherwise in the tobacco trade

EOID

S

M, if Reg_ 3RD = 1

1.4 Request for a facility identifier code

Item #

Field

Comments

Data Type Cardinalit y

Priority

Values

Message_Type

Identification of message type

Text

S

M

1-4

EO_ID

Economic operator identifier code

EOID

S

M

EO_CODE

Economic operator's confirmation code provided in response to the registration of economic operator

Text

S

M

F_street Facility’s street name and house number (or road number and kilometre) Text S M

F_municipality Facility’s municipality (city, town or village) Text S M

F_postcode Facility’s postal code Text S M ‘n/a’ is permitted value if no postal code has been assigned

F_A_info

Additional information on facility’s address (e.g. location in the shopping mall or industrial area)

Text

S

O

F_Country

Facility's country

Country

S

M

F_Type

Type of facility

Integer

S

M

1- manufacturing site with warehouse 2- standalone warehouse 3- retail outlet 4- other

F_Type_Other

Description of other facility

Text

S

M, if F_Type = 4

F_Status

Indication if a part of the facility has a tax (excise)  warehouse status

Boolean

S

M

0 - No 1 - Yes

F_Excise- Number1

Indication if the facility has an excise number issued by the competent authority for the purpose of identification of persons/premises

Boolean

S

M

0 - No SEED number 1 - SEED number exists

F_Excise- Number2

Facility's excise number issued by the competent authority for the purpose of identification of persons/premises

SEED

S

M, if F_ ExciseNumber 1 = 1

OtherFID_R

Indication if the facility has been allocated an identifier by another ID Issuer

Boolean

S

M

0 - No 1 - Yes (possible only for non-

Gibraltar facilities)

OtherFID_N

Facility identifier codes allocated by other ID Issuers

FID

M

M, if OtherFID_R = 1

PrevFID_B Indication if the facility was acquired from another operator and had already a facility identifier code Boolean S M

0 – No (first time registration) 1 - Yes

PrevFID_ID Previous facility identifier used by the former operator of the facility

FID

S

M, if PrevFID_B=1

Reg_3RD

Indication if the registration is made on behalf of a retail outlet operator not involved otherwise in the tobacco trade

Boolean

S

M

0 -  No 1 - Yes (possible only if F_Type = 3)

Reg_EOID

Identifier of the  economic operator that acts on  behalf  of the retail outlet operator not involved  otherwise  in  the tobacco trade

EOID

S

M, if Reg_ 3RD = 1

1.5 Correction of information concerning the facility identifier code

Item #

Field

Comments

Data Type Cardinalit y

Priority

Values

Message_Type

Identification of message type

Text

S

M

1-5

EO_ID

Economic operator identifier code

EOID

S

M

EO_CODE

Economic operator's confirmation code provided in response to the registration of economic operator

Text

S

M

F_ID

Facility identifier code

FID

S

M

F_street Facility’s street name and house number (or road number and kilometre) Text S M

F_municipality Facility’s municipality (city, town or village) Text S M

F_postcode Facility’s postal code Text S M ‘n/a’ is permitted value if no postal code has been assigned

F_A_info

Additional information on facility’s address (e.g. location in the shopping mall or industrial area)

Text

S

O

F_Country

Facility's country

Country

S

M

F_Type

Type of facility

Integer

S

M

1 - manufacturing site with warehouse 2 - standalone warehouse 3 - retail outlet 4 - other

F_Type_Other

Description of other facility

Text

S

M, if F_Type = 4

F_Status

Indication if a part of the facility has a tax (excise)  warehouse status

Boolean

S

M

0 - No 1 - Yes

F_Excise- Number1

Indication if the facility has an excise number issued by the competent authority for the purpose of identification of persons/premises

Boolean

S

M

0 - No SEED number 1 - SEED number exists

F_Excise- Number2

Facility's excise number issued by the competent authority for the purpose of identification of persons/premises

SEED

S

M, if F_ ExciseNumber 1 = 1

OtherFID_R

Indication if the facility has been allocated an identifier by another ID Issuer

Boolean

S

M

0 - No 1 - Yes (possible only for non- Gibraltar facilities)

OtherFID_N

Facility identifier codes allocated by other ID Issuers

FID

M

M, if OtherFID_R = 1

PrevFID_B Indication if the facility was acquired from another operator and had already a facility identifier code Boolean S M

0 – No (first time registration) 1 - Yes

PrevFID_ID Previous facility identifier used by the former operator of the facility

FID

S

M, if PrevFID_B=1

Reg_3RD

Indication if the registration is made on behalf of  the  retail outlet operator not involved otherwise in the tobacco trade

Boolean

S

M

0 - No 1 - Yes (possible only if F_Type = 3)

Reg_EOID

Identifier of the  economic operator that acts  on  behalf  of the retail outlet operator not involved  otherwise  in  the tobacco trade

EOID

S

M, if Reg_ 3RD = 1

1.6 De-registration of facility identifier code

Item #

Field

Comments

Data Type Cardinalit y

Priority

Values

Message_Type

Identification of message type

Text

S

M

1-6

EO_ID

Economic operator identifier code

EOID

S

M

EO_CODE

Economic operator's confirmation code provided in response to the registration of economic operator

Text

S

M

F_ID

Facility identifier code

FID

S

M

Reg_3RD

Indication if the de-registration is made on behalf of a retail outlet operator not involved otherwise in the tobacco trade

Boolean

S

M

0 - No 1 - Yes

Reg_EOID

Identifier of the  economic operator that acts  on  behalf  of the retail outlet operator not involved  otherwise  in  the tobacco trade

EOID

S

M, if Reg_ 3RD = 1

1.7 Request for a machine identifier code

Item #

Field

Comments

Data Type

Cardinality

Priority

Values

Message_Type

Identification of message type

Text

S

M

1-7

EO_ID

Economic operator identifier code

EOID

S

M

EO_CODE

Economic operator's confirmation code provided in response to the registration of economic operator

Text

S

M

F_ID

Facility identifier code

FID

S

M

PrevMID_B Indication if the object of this request was already registered, e.g. in relation to another facility identifier code Boolean S

M

0 – No (first time registration)

1 - Yes

PrevMID_ID Previous machine identifier used for the object of this request

MID

S

M, if PrevMID _B =1

M_entirety Indication if this request concerns the machine (v. a part of thereof) Boolean S

M

0 – No (machine part)

1 – Yes (machine)

P_Producer Part’s producer Text

S

M, if M_entiret y=0

P_Model Part’s model Text

S

M, if M_entiret y=0

P_Number Part’s serial number Text

S

M, if M_entiret y=0

P_Mobile Indication if this part is intended to be used with multiple machines (fixed v. mobile part) Boolean S

M, if M_entiret y=0

0 – No (fixed part)

1 – Yes (mobile part)

P_ATD1

Indication if an anti-tampering device in the sense of Article 2(7) records the functioning of this part Boolean S

M, if M_entiret y=0

0 - No

1 - Yes

P_ATD2 Anti-tampering device’s serial number Text

S

M, if M_entiret y=0 and P_ATD1= 1

P_Description Part’s description explaining its technical function Text

S

O

M_Producer Machine’s producer Text

S

M, if M_entiret y=1

M_Model Machine’s model Text

S

M, if M_entiret y=1

M_Number Machine’s serial number Text

S

M, if M_entiret y=1

M_parts Indication if the machine consists of multiple separately identifiable parts

Boolean S

M, if M_entiret y=1 and M_parts= 1

0 – No

1 - Yes

M_plist List of the identifiable parts MID M

M, if M_entiret y=1 and M_parts= 0

M_ATD Serial number of the anti- tampering device in the sense of Article 2(7) Text S

M, if M_entiret y=1

M_Capacity Maximum capacity over 24- hour production cycle expressed in unit packets Integer S

M, if M_entiret y=1

1.8 Correction of information concerning the machine identifier code

Item #

Field

Comments

Data Type

Cardinalit y

Priority

Values

Message_Type

Identification of message type

Text

S

M

1-8

EO_ID

Economic operator identifier code

EOID

S

M

EO_CODE

Economic operator's confirmation code provided in response to the registration of economic operator

Text

S

M

F_ID

Facility identifier code

FID

S

M

M_ID Machine identifier code (subject to the correct information) MID S M

PrevMID_B Indication if the object of this request was already registered, e.g. in relation to another facility identifier code Boolean S M 0 - No (first registration)

1 - Yes

PrevMID_ID Previous machine identifier code used for the object of this request MID S M, if PrevMID_B = 1

M_entirety Indication if this request concerns the machine (v. a part of thereof) Boolean Text M

0 - No (machine part)

1 - Yes (machine)

P_Producer Part’s producer Text S M, if M_entirety=0

P_Model Part’s model Text S M, if M_entirety=0

P_Number Part’s serial number Text S M, if M_entirety=0

P_Mobile Indication if this part is intended to be used with multiple machines (fixed v. mobile part) Boolean S M, if M_entirety=0 0 - No (fixed part)

1 - Yes (mobile part)

P_ATD1 Indication if an anti-tampering device in the sense of Article 2(7) records the functioning of this part Boolean S M, if M_entirety=0 0 – No )

1 – Yes

P_ATD2 Anti-tampering device’s serial number Text S M, if M_entirety=0 and P_ATD1=1

P_Description Part’s description explaining its technical function Text S O

M_Producer Machine's producer Text S M, if M_entirety=1

M_Model Machine's model Text S M, if M_entirety=1

M_Number Machine's serial number Text S M, if M_entirety=1

M_parts Indication if the machine consists of multiple separately identifiable parts Boolean S M, if M_entirety=1

M_plist List of the identifiable parts MID M M, if M_entirety=1

M_ATD Serial number of the anti- tampering device in the sense of Article 2(7) Text S M, if M_entirety=1 and M_parts=0

M_Capacity Maximum capacity over 24- hour production cycle expressed  in  unit packets Integer S M, if M_entirety=1

1.9 De-registration of machine identifier code

Item #

Field

Comments

Data Type

Cardinality

Priority

Values

Message_Type Identification of message type Text S M 1-9

EO_ID Economic operator identifier code EOID S M

EO_CODE Economic operator's confirmation code provided in response to the registration of economic operator Text S M

F_ID Facility identifier code FID S M

M_ID Machine identifier code MID S M

SECTION 2 Unique identifiers (UIs)

2.1 Request for unit level UIs

Item #

Field

Comments

Data Type

Cardinality

Priority

Values

Message_Type Identification of message typeText S M 2-1

EO_ID Economic operator identifier code of the submitting entity (either manufacturer or importer) EOID S M

F_ID Facility identifier code FID S M

Process_Type Indication if the production process involves machinery Boolean S M 0 – No (only for fully hand made products) 1 – Yes

M_ID Machine identifier code MID S M, if Process_ Type = 1

P_Type Type of tobacco product Integer S M 1 - Cigarette 2 - Cigar 3 -  Cigarillo 4. - Hand- rolling tobacco 5 - Pipe tobacco 6 -Waterpipe tobacco 7 - Oral tobacco 8 - Nasal tobacco 9 - Chewing tobacco 11 - Novel tobacco product 12 - Other (product placed on the market 24 months from the Implementati on Date, not covered by categories 1- 9)

P_OtherType Description of other type of tobacco product Text S M, if P_Type = 11

P_CN Combined Nomenclature (CN) code Text S O

P_Brand Brand of tobacco product Text S M

P_SubType_Exis t Indicates if the product ‘subt- type name’ exists. Subtype name provides further product identification beyond a product’s brand name Boolean S M 0- No 1- Yes

P_SubType_Na me The product ‘subtype name’ (if any) as marketed on its intended market Text S M, if P_SubType_Ex ist=1

P_units The number of individual units in the unit packet (number of sticks in the package). Integer S M, if P_Type = 1 or 2 or 3

P_weight Average gross weight of unit packet, including packaging, in grams with 0,1 gram accuracy Decimal S M

TP_ID Tobacco product identifier used in the CEG system TPID S M, if Intended_ Market is Gibraltar

TP_PN Tobacco product number used in the CEG system PN S M, if Intended_ Market is Gibraltar

Intended_ Market Intended country of retail saleCountry S M

Intended_ Route1 Indication if the product is intended to be moved across country boarders with terrestrial/ water/air transport Boolean S M 0 – No 1 – Yes

Intended_ Route2 The first country of terrestrial/ water/air transport after the product manufactured in or imported  leaves the country of manufacturing or the country of importation established on the basis of a check point on the land border, next seaport or next airport respectively Country S M, if Intended_ Route1 = 1

Import Indication if the product is imported into Gibraltar Boolean S M 0 – No 1 – Yes

Req_Quantity Requested quantity of unit packet level UIs Integer S M

2.2 Request for aggregated level UIs

Item # Field Comments Data Type Cardinality Priority Values

Message_Type Identification of message type Text S M 2-2

EO_ID Economic operator identifier code of the submitting entity EOID S M

F_ID Facility identifier code FID S M

Req_Quantity Requested quantity of aggregated level UIs Integer S M

2.3 Request for deactivation of UIs

Item #

Field

Comments

Data Type

Cardinalit y

Priority

Values

Message_Type Identification of message type Text S M 2-3

EO_ID Economic operator identifier code of the submitting entity EOID S M

Deact_Type Deactivation of unit packet or aggregated level UIs

Integer S M 1 - Unit packet level UIs 2. - Aggregated level UIs

Deact_Reason1Identification of the reason for deactivation Integer S M 1 - Product destroyed 2 - Product stolen 3 - UI destroyed 4 - UI stolen 5 - UI unused 6 - Other

Deact_Reason2Description of other reason Text S M, if Deact_ Reason1 = 6

Deact_Reason3Additional reason of the description Text S O

Deact_upUI List of unit packet level UIs to be deactivated upUI(L) or upUI(i) or upUI(s) M M, if Deact_ Type = 1

Deact_aUI List of aggregated level UIs to be deactivated aUI M M, if Deact_ Type = 2

2.4 Request for reactivation of UIs for products reported as stolen but recovered (only permitted if in preceding message type 2-3, field Deact_Reason1 = 2)

Item # Field Comments Data Type Cardin- ality Priority Values Message_Type Identification of message type Text S M 2-4

EO_ID Economic operator identifier code of the submitting entity EOID S M

F_ID Facility identifier code (facility of recovery) FID S M

React_Type Reactivation of unit packet or aggregated level UIs Integer S M 1 – Unit packet level UIs 2 – Aggregated level UIs

React_Reason Description of the context of reactivation Text S O

React_upUI List of unit packet level UIs to be reactivated upUI(L) or upUI(i) or upUI(s) M M, if React_Type = 1

React_aUI List of aggregated level UIs to be reactivated aUI M M, if React_Type = 2

SECTION 3 Recording and transmission of information on product movements

3A.1 Pairing between marked codes and virtual paired codes.

Field

Comments

Data Type

Cardinality

Priority

Values EO_ID Economic operator identifier code of the submitting entity EOID S M

Message_Time_Long The time that the message is first submitted to the Gateway, Long format. Time(L) S M

Event_Time Time of event occurrence Time(s) S M

upUI List of paired codes

S M

upID Code pairing detail

M M

upID Printed_Code Unit packet level UID marked on packs upUI(L) S M

upID Paired_Code Paired UID upUI(M) S M

3.1 Application of unit level UIs on unit packets

Item #

Field

Comments

Data Type

Cardinality

Priority

Values

Message_Type Identification of message type Text S M 3-1

EO_ID Economic operator identifier code of the submitting entity EOID S M

F_ID

Facility identifier code

FID

S

M

upUI_1

List of unit packet level UIs to be recorded (full length)

upUI(L)

M

M

upUI_2 List of corresponding unit packet level UIs to be recorded (as  visible in  human  readable format) indicated in the same order as upUI_1

upUI(s)

M

M

upUI_comment

Comments by the reporting entity

Text

S

O

3.2 Application of aggregated level UIs on aggregated packaging

Item #

Field

Comments

Data Type

Cardinalit y

Priority

Values

Message_Type

Identification of message type

Text

S

M

3-2

EO_ID

Economic operator identifier code of the submitting entity

EOID

S

M

F_ID

Facility identifier code

FID

S

M

Event_Time

Time of event occurrence

Time(s)

S

M

aUI

Aggregated level UI

aUI

S

M

Aggregation_ Type

Identification of aggregation type

Integer

S

M

1 - aggregation of only unit packet level UIs

2 - aggregation of only aggregated level UIs

3 - aggregation of both unit packet and aggregated level UIs

Aggregated_ UIs1

List of unit packet level UIs subject to aggregation

upUI(L)

M

M, if Aggregatio n_Type = 1 or 3

Aggregated_ UIs2

List of aggregated level UIs subject to further aggregation

aUI

M

M, if Aggregatio n_Type = 2 or 3

aUI_comment

Comments by the reporting entity

Text

S

O

3.3 Dispatch of tobacco products from a facility

Item #

Field

Comments

Data Type

Cardinalit y

Priority

Values

Message_Type

Identification of message type

Text

S

M

3-3

EO_ID

Economic operator identifier code of the submitting entity

EOID

S

M

Event_Time

Intended time of event occurrence

Time(s)

S

M

F_ID

Dispatch facility identifier code

FID

S

M

Destination_ ID1

Indication of destination type: if the destination facility is located in Gibraltar and if it is delivery to a vending machine (VM) or by means of a vending van (VV) delivering to multiple retail outlets in quantities  that have not been predetermined in advance of the delivery

Integer

S

M

1 - Non Gibraltar dest. 2 - Gibraltar destination other than VM – fixed quantity delivery

3 - Gibraltar VM(s)

4 - Gibraltar destination other than VM – delivery with VV

Destination_ ID2

Destination facility identifier code

FID

S

M, if Destination _ID1 = 2

Destination_ ID3

Destination facility identifier code(s) possible multiple vending machines

FID

M

M, if Destination _ID1 = 3

Destination_ ID4

Destination facility identifier code(s)

FID

M

M, if Destination _ ID1 = 4

Destination_ ID5

Destination facility's full address: street, house number, postal code, city

Text

S

M, if Destination _ID1 = 1

Transport_ mode

Mode of transport by which the product leaves the facility

Integer

S

M

0 - Other 1 - Sea Transport 2 - Rail transport 3 - Road transport 4 - Air transport 5 - Postal consignment 6 - Fixed transport installations 7 - Inland waterway transport

Transport_ vehicle

Identification of the vehicle (i.e. number plates, train number, plane/flight  number,  ship name or other identification)

Text

S

M

‘n/a’ is permitted value if Transport_mode = 0 and product movement takes place between adjacent facilities and is delivered manually

Transport_ cont1

Indication if the transport is containerised and uses an individual transport unit code (e.g. SSCC)

Boolean

S

M

0 – No

1.- Yes

Transport_ cont2 Individual transport unit code of the container ITU S M, if Transport_c ont1 = 1

Transport_s1 Indication if the dispatch takes place with the logistic/ postal operator who operates its own track and trace system. Only for small quantities of tobacco products (net weight of the products dispatched below 10kg) destined for exports to other countries Boolean S M

0 – No

1 – Yes

Transport_s2 The logistic operator's tracking number Text S M, if Transport_s 1= 1

Exp_ Declaration Indication if the Movement Reference Number (MRN) has been issued by the customs office Boolean S M

0 – No

1 – Yes

Exp_ Declaration- Number Movement Reference Number (MRN) MRN S M, if Exp_ Declaration = 1

UI_Type Identification of UI types in the dispatch (recorded at the highest level of available aggregation) Integer S M 1 - only unit packet level UIs 2 - only aggregated level UIs 3 - both unit packet and aggregated level UIs

upUIs List of unit packet level UIs subject to the dispatch upUI(L) M M, if  UI_ Type = 1 or 3

aUIs List of aggregated level UIs subject to the dispatch aUI M M, if  UI_ Type = 2 or 3

Dispatch_ comment

Comments by the reporting entity

Text

S

O

3.4 Arrival of tobacco products at a facility

Item #

Field

Comments

Data Type

Cardinality

Priority

Values

Message_Type

Identification of message type

Text

S

M

3-4

EO_ID

Economic operator identifier code of the submitting entity

EOID

S

M

F_ID

Arrival facility identifier code

FID

S

M

Event_Time

Time of event occurrence

Time(s)

S

M

Product_Return

Indication if the arriving products are a return following complete or partial non- delivery

Boolean

S

M

0 – No

1 – Yes

UI_Type

Identification of UI types received (recorded at the highest level of available aggregation)

Integer

S

M

1 - only unit packet level UIs 2 - only aggregated level UIs 3 - both unit packet and aggregated level UIs

upUIs

List of Unit packet level UIs received

upUI(L)

M

M, if  UI_ Type = 1 or 3

aUIs

List of aggregated level UIs received

aUI

M

M, if  UI_ Type = 2 or 3

Arrival_ comment

Comments by the reporting entity

Text

S

O

3.5 Trans-loading

Item #

Field

Comments

Data Type

Cardinalit y

Priority

Values

Message_Type

Identification of message type

Text

S

M

3-5

EO_ID

Economic operator identifier code of the submitting entity

EOID

S

M

Event_Time

Intended time of event occurrence

Time(s)

S

M

Destination_ ID1

Indication if the destination facility is located in Gibraltar

Boolean

S

M

0 - No

1 - Yes

Destination_ ID2 Destination facility identifier code FID S M, if Destination _ID1=1

Destination_ ID3 Destination facility’s street name and house number (or road number and kilometre) Text S M, if Destination _ID1=0

Destination_ ID4 Destination facility’s municipality (city, town or village) Text S M, if Destination _ID1=0

Destination_ ID5 Destination facility’s postal code Text S M, if Destination _ID1=0 ‘n/a’ is permitted value if no postal code has been assigned

Destination_ ID6

Destination facility’s country

Country

S

M, if Destination _ID1=0

Transport_ mode Mode of transport to which the product is trans-loaded Integer S M

0 - Other 1 - Sea Transport 2 - Rail transport 3 - Road transport 4 - Air transport 5 - Postal consignment 6 - Fixed transport installations 7 - Inland waterway transport

Transport_ vehicle Identification of the vehicle (i.e. number plates, train number, plane/flight  number,  ship name or other identification) Text S M

Transport_ cont1 Indication if the transport is containerised and uses an indi- vidual transport unit code (e.g. SSCC) Boolean S M

0 - No

1 - Yes

Transport_ cont2 Individual transport unit code of the container ITU S M, if Transport_ cont1 = 1

EMCS Dispatch under the Excise Movement and Control System (EMCS) Boolean S M

0 – No

1 - Yes

EMCS_ARC Administrative Reference Code (ARC) ARC S M, if EMCS = 1

UI_Type Identification of UI types subject to the trans-loading (recorded at the highest level of available aggregation) Integer S M 1 - only unit packet level UIs 2 – only aggregated level UIs 3 – both unit packet and aggregated level UIs

upUIs List of unit packet level UIs subject to the trans-loading upUI(L) M M, if UI_ Type = 1 or 3

aUIs List of aggregated level UIs subject to the trans-loading aUI M M, if UI_ Type = 2 or 3

Transloading_ comment Comments by the reporting entity Text S O

3.6 Disaggregation of aggregated level UIs

Item #

Field

Comments

Data Type

Cardinalit y

Priority

Values

Message_Type Identification of message type Text S M 3-6

EO_ID Economic operator's identifier EOID S M

F_ID Facility's identifier FID S M

Event_Time Time of event occurrence Time(s) S M

aUI Aggregated level UI subject to disaggregation aUI S M

disaUI_ comment Comments by the reporting entity Text S O

3.7 Report of delivery carried out with a vending van to retail outlet (required if in message type 3-3, field Destination_ID1 = 4)

Item #

Field

Comments

Data Type

Cardinalit y

Priority

Values

Message_Type Identification of message type Text S M 3-7

EO_ID Economic operator identifier code of the submitting entity EOID S M

F_ID Facility identifier code of retail outlet FID S M

Event_Time Time of event occurrence Time(s) S M

UI_Type Identification of UI  types delivered (recorded at the highest level of available aggregation) Integer S M 1 - only unit packet level UIs 2 - only aggregated level UIs 3 - both unit packet and aggregated level UIs

upUIs List of  unit packet level UIs delivered upUI(L) M M, if  UI_ Type = 1 or 3

aUIs List of aggregated level UIs delivered aUI M M, if  UI_ Type = 2 or 3

Delivery_ comment Comments by the reporting entity Text S O

3.8 Dispatch of tobacco products from a facility to laboratories, waste disposal centres, national authorities, international governmental organisations, embassies and military bases

Item #

Field

Comments

Data Type

Cardinalit y

Priority

Values

Message_Type Identification of message type Text S M 3-8

EO_ID Economic operator identifier code of the submitting entity EOID S M

Event_Time Intended time of event occurrence Time(s) S M

F_ID Despatch facility identifier codeFID S M

Destination_1 Indication of destination type Integer S M 1 – Laboratory 2 – Waste disposal centre 3 – National authority 4 – International governmental organisation 5 – embassy 6 – military base

Destination_2 Destination’s street name and house number (or road number and kilometre) Text S M

Destination_3 Destination’s municipality (city, town or village) Text S M

Destination_4 Destination’s postal code Text S M ‘n/a’ is permitted if no postal code has been assigned

Destination_5 Destination’s country Country S M

Transport_ mode Mode of transport by which the product leaves the facility, see Annex II, Code List 7 of Regulation (EC) No 684/2009 Integer S M 0 – Other 1 – Sea Transport 2 – Rail transport 3 – Road transport 4 – Air transport 5 Postal consignment 6 – Fixed transport installations 7 – Inland waterway transport

Transport_ vehicle Identification of the vehicle (i.e. number plates, train number, plane/flight number, ship name or other identification) Text S M ‘n/a’ is permitted value if Transport_mode = 0 and product movement takes place between adjacent facilities and is delivered manually

Transport_cont 1 Indication if the transport is containerised and uses an indi vidual transport unit code (e.g. SSCC) Boolean S M

0 - No

1 - Yes

Transport_ cont2 Individual transport unit code of the container Integer S M, if Transport_ cont1 = 1

UI_Type Identification of UI  types delivered (recorded at the highest level of available aggregation) Integer S M 1 - only unit packet level UIs 2 - only aggregated level UIs 3 - both unit packet and aggregated level UIs

upUIs List of  unit packet level UIs delivered upUI(L) M M, if  UI_ Type = 1 or 3

aUIs List of aggregated level UIs delivered aUI M M, if  UI_ Type = 2 or 3

S_Dispatch_ comment Comments by the reporting entity Text S O

SECTION 4 Transactional events

4.1 Issuing of the invoice

Item #

Field

Comments

Data Type

Cardinalit y

Priority

Values

Message_Type Identification of message type Text S M 4-1

EO_ID Economic operator identifier code of the submitting entity EOID S M

Event_Time Time of event occurrence Time(s) S M

Invoice_Type1 Type of the invoice Integer S M 1 - Original 2 - Correction 3 - Other

Invoice_Type2 Description of the other type of the invoice Text S M, if Invoice_ Type1 = 3

Invoice_ Number Number of the invoice Text S M

Invoice_Date Date of the invoice Date S M

Invoice_Seller Identity of the seller EOID S M

Invoice_Buyer 1 Indication if the buyer is located in Gibraltar Boolean S M

0 – No

1 - Yes

Invoice_Buyer 2 Identity of the buyer EOID S M, if Invoice_ Buyer1 = 1

Buyer_Name Buyer's registered legal name Text S M, if Invoice_ Buyer1 = 0

Buyer_ Address _1 Buyer’s street name and house number (or road number and kilometre) Text S M, if Invoice_ Buyer1 = 0

Buyer_ Address _2 Buyer’s municipality (city, town or village) Text S M, if Invoice_ Buyer1 = 0

Buyer_ Address _3 Buyer’s postal code Text S M, if Invoice_ Buyer1 = 0 ‘n/a’ is permitted value if no postal code has been assigned

Buyer_ CountryReg Buyer's country of registration Country S M, if Invoice_ Buyer1 = 0

Buyer_TAX_N Buyer's tax registration number Text S M, if Invoice_ Buyer1 = 0

First_Seller_ GI Indication if the invoice is issued by the first seller in Gibraltar, i.e. the Gibraltar manufacturer or the importer, and the product is destined for the Gibraltar market Boolean S M

0 – No

1 - Yes

Product_ Items_1 List of TPIDs corresponding to the product items listed on the invoice TPID M M, if First_ Seller_GI = 1

Product_ Items_2 List of product numbers corresponding to the product items listed on the invoice (in the same order as Product_Items_1) PN M M, if First_ Seller_GI = 1

Product_Price Net unit packet price per each pair of TPID and product number (in the same order as Product_ Items_1) Decimal M M, if First_ Seller_GI = 1

Invoice_Net Total net amount of the invoice Decimal S M

Invoice_ Currency Currency of the invoice Currenc y S M

UI_Type Identification of UI types covered by the invoice (recorded at the highest level of available aggregation) Integer S M 1 – only unit packet level UIs 2 – only aggregated level UIs 3 – both unit packet and aggregated level UIs

upUIs List of unit packet level UIs covered by the invoice upUI(L) M M, if  UI_ Type = 1 or 3

aUIs List of aggregated level UIs covered by the invoice aUI M M, if  UI_ Type = 2 or 3

Invoice_ comment Comments by the reporting entity Text S O

4.2 Issuing of the order number

Item #

Field

Comments

Data Type

Cardinalit y

Priority

Values

Message_Type Identification of message type Text S M 4-2

EO_ID Economic operator identifier code of the submitting entity EOID S M

Event_Time Time of event occurrence Time(s) S M

Order_Number Number of the purchase order Text S M

Order_Date Date of the purchase order Date S M

UI_Type Identification of UI types covered by the purchase order (recorded at the highest level of available aggregation) Integer S M 1 – only unit packet level UIs 2 – only aggregated level UIs 3 – both unit packet and aggregated level UIs

upUIs List of unit packet level UIs covered by the purchase order upUI(L) M M, if  UI_ Type = 1 or 3

aUIs List of aggregated level UIs covered by the purchase order aUI M M, if  UI_ Type = 2 or 3

Order_ comment Description of the reason for delayed recording of the purchase order Text S O

4.3 Receipt of the payment

Item #

Field

Comments

Data Type

Cardina lity

Priority

Values

Message_Type Identification of message type Text S M 4-3

EO_ID Economic operator identifier code of the submitting entity EOID S M

Event_Time Time of event occurrence Time(s) S M

Payment_Date Date of the payment receipt Date S M

Payment_Type Type of payment Integer S M 1 – bank transfer 2 – bank card 3 - cash 4 - other

Payment_ Amount Amount of the payment Decimal S M

Payment_ Currency Currency of the payment Currenc y S M

Payment_ Payer1 Indication if the payer is located in Gibraltar Boolean S M

0 – No

1 - Yes

Payment_ Payer2 Identity of the payer EOID S M, if Payment_ Payer1 = 1

Payer_Name Payer's registered legal name Text S M, if Payment_ Payer1 = 0

Payer_Address _1 Payer's street name and house number (or road number and kilometre) Text S M, if Payment_ Payer1 = 0

Payer_Address _2 Payer’s municipality (city, town or village) Text S M, if Payment_ Payer1 = 0

Payer_Address _3 Payer’s postal code Text S M, if Payment_ Payer1 = 0 ‘n/a’ is permitted value if no postal code has been assigned

Payer_Country - Reg Payer's country of registration Country S M, if Payment_ Payer1 = 0

Payer_TAX_N Payer's tax registration number Text S M, if Payment_ Payer1 = 0

Payment_Re- cipient Identity of the recipient EOID S M

Payment_ Invoice Indication if the payment corresponds to the existing invoice Boolean S M

0 – No

1 - Yes

Invoice_Paid Number of the invoice paid with the payment Text S M, if Payment_ Invoice = 1

UI_Type Identification of UI types covered by the payment (recorded at the highest level of available aggregation) Integer S M, if Payment_ Invoice = 0 1– only unit packet level UIs 2– only aggregated level UIs 3 – both unit packet and aggregated level UIs

upUIs List of unit packet level UIs covered by the payment upUI(L) M M, if Payment_ Invoice = 0 and UI_Type = 1 or 3 aUIs List of aggregated level UIs covered by the payment aUI M M, if Payment_ Invoice = 0 and UI_Type = 2 or 3

Payment_ comment Comments by the reporting entity Text S O

SECTION 5 Recalls

5. Recalls of requests, operational and transactional messages (possible for message types 2-1, 2-2, 2-3 (only within 24 hours from the original reporting of message 2-3, for Deact_Reason1 other than ‘2 – Product stolen’), 3-1 to 3-8, 4-1, 4-2 and 4-3)

Item #

Field

Comments

Data Type

Cardina lity

Priority

Values

Message_Type Identification of message type Text S M 5

EO_ID Economic operator identifier code of the submitting entity EOID S M

Recall_CODE Message recall code provided to the message sender in the acknowledgement of the original message to be recalled Text S M Recall_CODE

Recall_ Reason1 Reason for recalling the original message Integer S M 1 - reported event did not materialise (only for message types 3-3, 3-5 and 3-8)

2 - message contained erroneous information

3 - other

Recall_ Reason2 Description of the reason for recalling the original message Text S M, if Recall_ Reason1 = 3

Recall_ Reason3 Any additional explanations  on the reason for recalling the original message Text S O

Notice: A recall with respect to operational and logistic events results in flagging the recalled message as cancelled but does not lead to the deletion of the existing database record.
