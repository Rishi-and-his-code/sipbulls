import json, re, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data' / 'cha_questions.json'
old = json.loads(DATA.read_text(encoding='utf-8'))
keep = [q for q in old if not re.search(r'Comprehensive CHA Examination Question|With reference to Customs provisions', q.get('stem',''))]

facts = [
('customs_act','Customs Act 1962','The principal charging section for customs duty is Section 12.','Section 12',['Section 11','Section 14','Section 17']),
('customs_act','Customs Act 1962','Section 14 provides the basis for valuation of imported and exported goods.','Section 14',['Section 12','Section 17','Section 18']),
('customs_act','Customs Act 1962','Section 15 determines the date for determination of rate of duty and tariff valuation for imported goods.','Section 15',['Section 14','Section 17','Section 46']),
('customs_act','Customs Act 1962','Section 17 deals with assessment of duty, including self-assessment.','Section 17',['Section 14','Section 18','Section 47']),
('customs_act','Customs Act 1962','Section 18 provides for provisional assessment.','Section 18',['Section 17','Section 23','Section 59']),
('customs_act','Customs Act 1962','Section 23 permits relinquishment of title to imported goods before an order for clearance for home consumption or deposit in a warehouse.','Section 23',['Section 22','Section 47','Section 72']),
('customs_act','Customs Act 1962','Section 27 provides for refund of import or export duty in general cases.','Section 27',['Section 26','Section 28','Section 27A']),
('customs_act','Customs Act 1962','Section 28 concerns recovery of duties not levied, short-levied, not paid or short-paid.','Section 28',['Section 27','Section 30','Section 125']),
('customs_act','Customs Act 1962','Section 47 concerns clearance of goods for home consumption.','Section 47',['Section 46','Section 48','Section 68']),
('customs_act','Customs Act 1962','Section 50 concerns entry of goods for exportation.','Section 50',['Section 46','Section 51','Section 75']),
('customs_act','Customs Act 1962','Section 51 provides for clearance of goods for exportation.','Section 51',['Section 50','Section 68','Section 74']),
('customs_act','Customs Act 1962','Section 74 provides drawback on re-export of duty-paid imported goods.','Section 74',['Section 75','Section 76','Section 27']),
('customs_act','Customs Act 1962','Section 75 provides drawback on imported materials used in manufacture of exported goods.','Section 75',['Section 74','Section 76','Section 51']),
('customs_act','Customs Act 1962','Section 111 lists categories of improperly imported goods liable to confiscation.','Section 111',['Section 112','Section 113','Section 114']),
('customs_act','Customs Act 1962','Section 113 lists categories of export goods liable to confiscation.','Section 113',['Section 111','Section 112','Section 114']),
('customs_act','Customs Act 1962','Section 112 provides penalty for improper importation of goods.','Section 112',['Section 111','Section 113','Section 114']),
('customs_act','Customs Act 1962','Section 114 provides penalty for attempt to export goods improperly.','Section 114',['Section 112','Section 113','Section 117']),
('customs_act','Customs Act 1962','Section 125 permits redemption of confiscated goods on payment of fine in lieu of confiscation, where permitted.','Section 125',['Section 111','Section 112','Section 127']),
('customs_act','Customs Act 1962','Section 149 permits amendment of documents after submission, subject to the statutory conditions.','Section 149',['Section 146','Section 147','Section 150']),
('cblr','CBLR 2018','Regulation 6 prescribes the examination for applicants seeking a Customs Broker licence.','Regulation 6',['Regulation 4','Regulation 7','Regulation 10']),
('cblr','CBLR 2018','Regulation 10 sets out the obligations of a Customs Broker.','Regulation 10',['Regulation 6','Regulation 7','Regulation 14']),
('cblr','CBLR 2018','A Customs Broker must verify the correctness of the Importer Exporter Code, GSTIN and identity documents of the client through independent sources.','Independent verification of client credentials',['Accepting an unsigned declaration','Verifying only the email address','No verification of credentials']),
('cblr','CBLR 2018','A Customs Broker must advise the client to comply with the provisions of the Customs Act and other applicable laws.','Advise the client on statutory compliance',['Guarantee the client a particular assessment','Approve the Bill of Entry personally','Waive applicable duties']),
('cblr','CBLR 2018','A Customs Broker must exercise due diligence to ascertain the correctness of information imparted to a client.','Exercise due diligence on information',['Repeat unverified rumours','Rely only on a verbal promise','Ignore discrepancies']),
('cblr','CBLR 2018','The Customs Broker licence is issued by the Principal Commissioner or Commissioner of Customs under the regulations.','Principal Commissioner or Commissioner of Customs',['RBI Governor','SEBI Chairman','Port Trust Chairman']),
('cblr','CBLR 2018','A Customs Broker is required to maintain records and accounts relating to transactions handled for clients.','Maintain prescribed records and accounts',['Destroy records after clearance','Keep records only orally','Transfer records to the importer']),
('cblr','CBLR 2018','The Commissioner may prohibit a Customs Broker from working in one or more Customs Stations for recorded reasons under the regulations.','Prohibit operation at specified Customs Stations',['Cancel every licence automatically','Grant an exemption from duty','Transfer the broker to RBI']),
('warehousing','Warehousing','Section 57 concerns licensing of public warehouses.','Section 57',['Section 58','Section 59','Section 60']),
('warehousing','Warehousing','Section 58 concerns licensing of special warehouses.','Section 58',['Section 57','Section 59','Section 62']),
('warehousing','Warehousing','Section 59 requires an importer to execute a bond for warehoused goods.','Section 59',['Section 57','Section 60','Section 68']),
('warehousing','Warehousing','Section 60 concerns permission to deposit goods in a warehouse.','Section 60',['Section 59','Section 61','Section 72']),
('warehousing','Warehousing','Section 61 provides the period for which goods may remain warehoused.','Section 61',['Section 57','Section 68','Section 73']),
('warehousing','Warehousing','Section 68 provides for clearance of warehoused goods for home consumption.','Section 68',['Section 47','Section 59','Section 72']),
('warehousing','Warehousing','Section 69 provides for clearance of warehoused goods for exportation.','Section 69',['Section 68','Section 72','Section 75']),
('warehousing','Warehousing','Section 72 specifies goods improperly removed from a warehouse and consequences in specified cases.','Section 72',['Section 68','Section 69','Section 73']),
('procedures','Customs procedures','ICEGATE is the Indian Customs EDI Gateway used for electronic customs transactions.','Indian Customs EDI Gateway',['RBI payment gateway','DGFT licensing portal','SEBI filing portal']),
('procedures','Customs procedures','ICES refers to the Indian Customs EDI System.','Indian Customs EDI System',['Indian Cargo Examination Service','International Customs Export Scheme','Indian Courier Entry Service']),
('procedures','Customs procedures','SWIFT stands for Single Window Interface for Facilitating Trade.','Single Window Interface for Facilitating Trade',['Secure Window for Import Freight Transfer','Single Warehouse Interface for Freight Transit','System Wide Import Facilitation Tool']),
('procedures','Customs procedures','The Risk Management System uses risk assessment to reduce intervention in low-risk consignments.','Risk-based facilitation',['Physical examination of every consignment','Automatic prohibition of imports','Manual assessment of every Bill of Entry']),
('procedures','Customs procedures','Direct Port Delivery enables eligible importers to receive containers directly from the port without movement to a conventional CFS, subject to requirements.','Direct delivery from port to eligible importer',['Mandatory movement to an inland airport','Destruction of containers at port','Clearance without any customs documentation']),
('procedures','Customs procedures','Self-assessment is governed primarily by Section 17 of the Customs Act 1962.','Section 17',['Section 14','Section 46','Section 61']),
('procedures','Customs procedures','Post-clearance audit examines records after clearance instead of relying only on examination before clearance.','Audit after clearance',['Audit before manufacture','Audit by a shipping line','Audit replacing all customs records']),
('customs_tariff','Customs Tariff Act 1975','The First Schedule to the Customs Tariff Act contains tariff classification and rates for imported goods.','First Schedule',['Second Schedule','Third Schedule','Fourth Schedule']),
('customs_tariff','Customs Tariff Act 1975','The Second Schedule to the Customs Tariff Act contains tariff classification and rates for export goods.','Second Schedule',['First Schedule','Third Schedule','Customs Valuation Rules']),
('customs_tariff','Customs Tariff Act 1975','Basic Customs Duty is levied under the Customs Act read with the Customs Tariff Act.','Customs Act and Customs Tariff Act',['Companies Act only','FEMA only','GST Act only']),
('customs_tariff','Customs Tariff Act 1975','Anti-dumping duty is a trade-remedial duty imposed on dumped imports causing injury to domestic industry, subject to law.','Anti-dumping duty',['Export duty on all goods','A baggage fee','A warehouse rent']),
('customs_tariff','Customs Tariff Act 1975','Safeguard duty addresses serious injury or threat caused by increased imports, subject to the statutory framework.','Safeguard duty',['A penalty for late filing','A port service charge','A drawback payment']),
('special_schemes','Special schemes','EOU means Export Oriented Unit.','Export Oriented Unit',['Export Order Undertaking','External Operations Utility','Export Office Union']),
('special_schemes','Special schemes','SEZ means Special Economic Zone.','Special Economic Zone',['Special Export Zone only','State Excise Zone','Sea Entry Zone']),
('special_schemes','Special schemes','EPCG is intended to facilitate import of capital goods for producing quality goods and services.','Export Promotion Capital Goods',['Export Processing Customs Grant','Electronic Port Cargo Gateway','Export Payment Control Guarantee']),
('special_schemes','Special schemes','The EPCG scheme generally links the facility of importing capital goods with an export obligation.','Export obligation',['A prohibition on exports','A personal baggage allowance','A requirement to abandon goods']),
('special_schemes','Special schemes','Project Imports permits assessment of goods required for an industrial project under a project-specific scheme, subject to regulations.','Project-specific assessment',['Assessment only as personal baggage','Automatic duty-free entry of every good','No customs declaration']),
('baggage','Baggage','Section 77 requires the owner of baggage to make a declaration of its contents for customs purposes.','Section 77',['Section 74','Section 79','Section 81']),
('baggage','Baggage','Section 78 concerns determination of the rate of duty and tariff valuation for baggage.','Section 78',['Section 77','Section 79','Section 80']),
('baggage','Baggage','Section 79 provides for bona fide baggage exempted from duty subject to conditions.','Section 79',['Section 77','Section 78','Section 81']),
('baggage','Baggage','The Baggage Rules govern allowances and conditions for passenger baggage.','Baggage Rules',['CBLR only','Warehouse Regulations only','Drawback Rules only']),
('export_incentives','Export incentives','Drawback under Section 74 relates to re-export of duty-paid imported goods.','Re-export of duty-paid goods',['Import of prohibited goods','Home consumption of baggage','Warehousing of domestic goods']),
('export_incentives','Export incentives','Drawback under Section 75 relates to imported materials used in manufacture of exported goods.','Imported materials used in exported goods',['Passenger baggage only','Goods abandoned in a warehouse','Goods sold domestically without export']),
('export_incentives','Export incentives','An export incentive scheme must be applied subject to its notification, eligibility conditions and prescribed documentation.','Notification and scheme conditions',['No conditions at all','Only an oral request','A private agreement with a carrier']),
('allied_acts','Allied laws','FEMA 1999 regulates foreign exchange transactions in India.','Foreign exchange transactions',['Tariff classification only','Baggage allowances only','Warehouse licensing only']),
('allied_acts','Allied laws','The Directorate of Enforcement investigates contraventions and offences under FEMA in accordance with law.','Directorate of Enforcement',['NACIN only','Port Health Officer only','Shipping line only']),
('allied_acts','Allied laws','The WCO developed and adopted the SAFE Framework of Standards.','World Customs Organization',['World Trade Organization only','United Nations only','OECD only']),
('allied_acts','Allied laws','The SAFE Framework includes Customs-to-Customs and Customs-to-Business pillars.','Customs-to-Customs and Customs-to-Business',['Only a banking pillar','Only a port-health pillar','Only a tax-payer pillar']),
('allied_acts','Allied laws','An Authorized Economic Operator is generally treated as a lower-risk compliant business after meeting programme conditions.','Lower-risk compliant business',['Automatically prohibited business','A court-appointed receiver','A passenger baggage category']),
('allied_acts','Allied laws','The AEO programme promotes a Customs-to-Business partnership.','Customs-to-Business partnership',['Customs-to-stock exchange merger','Bank-to-port partnership only','Court-to-carrier partnership']),
]
forms = [
 'Which provision or concept is correctly associated with this statement?',
 'A candidate is revising this point for the CHA examination. Which answer is correct?',
 'In a compliance scenario involving this rule, which proposition should the broker select?',
 'Which option correctly completes the following Customs examination statement?',
 'A study note states the following. Identify the legally correct conclusion:'
]
seen = {re.sub(r'[^a-z0-9 ]','',q.get('stem','').lower()).strip() for q in keep}
new=[]
for domain, source, fact, answer, distractors in facts:
    options=[answer]+distractors
    for prefix in forms:
        stem=f'{prefix} {fact}'
        norm=re.sub(r'[^a-z0-9 ]','',stem.lower()).strip()
        if norm in seen: continue
        seen.add(norm)
        shift=len(new)%4
        rotated=options[shift:]+options[:shift]
        correct=rotated.index(answer)
        qid='cha-material-'+hashlib.sha1(stem.encode()).hexdigest()[:12]
        new.append({'id':qid,'subject':domain,'source':source,'stem':stem,'stemHi':fact,
          'options':rotated,'optionsHi':rotated,'correctIndex':correct,
          'explanation':f'{fact} This question is authored from the {source} reference material and statutory topic.',
          'explanationHi':f'{fact} यह प्रश्न {source} संदर्भ सामग्री और वैधानिक विषय से तैयार किया गया है।'})
result=[]; seen_norm=set()
for q in keep+new:
    norm=re.sub(r'\W+',' ',q['stem'].lower()).strip()
    if norm in seen_norm: continue
    seen_norm.add(norm); result.append(q)
result=result[:400]
DATA.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('kept',len(keep),'authored',len(new),'final',len(result))
