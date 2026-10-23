import json
from pathlib import Path

path = Path(__file__).resolve().parent.parent / 'data' / 'cha_questions.json'
bank = json.loads(path.read_text(encoding='utf-8'))

questions = [
('Which international organisation developed and adopted the SAFE Framework of Standards?', ['World Trade Organization (WTO)', 'World Customs Organization (WCO)', 'United Nations (UN)', 'Organisation for Economic Co-operation and Development (OECD)', 'European Union (EU)'], 1, 'AEO - December 2019'),
('In which year was the SAFE Framework of Standards adopted by the World Customs Organization?', ['2003', '2004', '2005', '2006', '2011'], 2, 'AEO - December 2019'),
('Which is a basic aim of the SAFE Framework of Standards?', ['Promote trade facilitation with an integrated global supply chain', 'Act as a deterrent to international terrorism', 'Secure revenue collections', 'All of the above', 'None of the above'], 3, 'AEO - December 2019'),
('Which is a core element of the SAFE Framework of Standards?', ['Advance electronic information about inbound, outbound and transit shipments', 'Consistent risk management for security threats', 'Outbound inspection of high-risk consignments', 'Benefits for businesses meeting supply-chain security standards', 'All of the above'], 4, 'AEO - December 2019'),
('The SAFE Framework of Standards deals with supply-chain management by which transport modes?', ['Air only', 'Road only', 'Rail only', 'Sea only', 'All modes of transport'], 4, 'AEO - December 2019'),
('Which pillars are associated with the WCO SAFE Framework?', ['Customs-to-Customs', 'Customs-to-Business', 'Customs-to-Other Government and Inter-Governmental Agencies', 'All of the above', 'None of the above'], 3, 'AEO - December 2019'),
('An Authorized Economic Operator is generally treated by Customs as a:', ['Low-risk compliant business', 'High-risk business', 'Moderate-risk business', 'Prohibited business', 'Business with no legal status'], 0, 'AEO - December 2019'),
('The essence of the AEO programme is to promote and facilitate:', ['Business-to-business partnership', 'Customs-to-business partnership', 'WCO-to-business partnership', 'Only cooperation between ports', 'Only cooperation between banks'], 1, 'AEO - December 2019'),
('Which condition is considered before granting AEO status?', ['Financial viability', 'Demonstrated compliance with Customs requirements', 'Satisfactory commercial-record management', 'Approved security and safety standards', 'All of the above'], 4, 'AEO - December 2019'),
('Which is a benefit generally associated with AEO status?', ['Reduced bank guarantee where applicable', 'Faster approvals or fee relief where provided', 'Reduced procedural requirements', 'Reduced examination norms subject to the scheme', 'All of the above'], 4, 'AEO - December 2019'),
('How many years of Customs-related business experience was specified in the referenced AEO study material for an eligible supply-chain entity?', ['No experience', 'One year', 'Two years', 'Three years', 'Five years'], 3, 'AEO - December 2019'),
('Who grants AEO status in a country?', ['World Customs Organization', 'National Customs Administration', 'National police agency', 'Trade chamber', 'Export Promotion Council'], 1, 'AEO - December 2019'),
('Which document is not normally listed among AEO applicant security and process documents in the referenced material?', ['Security plan', 'Site plan', 'Process map', 'Business plan', 'Self-assessment form'], 3, 'AEO - December 2019'),
('What is the purpose of a Mutual Recognition Agreement for AEO programmes?', ['Avoid double taxation', 'Mutually recognise AEO certification granted by respective Customs administrations', 'Exchange all import data in real time', 'Replace national Customs laws', 'Create a common currency'], 1, 'AEO - December 2019'),
('ISCM in the AEO study material stands for:', ['Integral Supply Chain Mechanism', 'Integrated Supply Chain Management', 'Internal Statutory Compliance Mechanism', 'Integrated Supply Chain Mechanism', 'International Supply Chain Management'], 1, 'AEO - December 2019'),
('Which is a key theme of the Customs-to-Business pillar?', ['Partnership', 'Manual data entry', 'Strict physical control of every shipment', 'No communication', 'Removal of technology'], 0, 'AEO - December 2019'),
('An AEO certificate may be suspended when:', ['There is reasonable belief of a serious Customs infringement', 'Conditions or criteria are not met and remedial action is not taken', 'Either of the above circumstances applies', 'The business exports one shipment', 'A Bill of Entry is filed electronically'], 2, 'AEO - December 2019'),
('The AEO programme is intended to improve Customs capability to:', ['Detect high-risk consignments', 'Eliminate all risk from international trade', 'Stop all imports', 'Replace all Customs officers', 'Remove advance cargo information'], 0, 'AEO - December 2019'),
('AEO benefits are granted only after the applicant:', ['Meets the applicable eligibility and security criteria', 'Requests exemption orally', 'Stops maintaining records', 'Avoids Customs verification', 'Surrenders its IEC'], 0, 'AEO - December 2019'),
('The SAFE Framework is primarily concerned with security and facilitation of the:', ['International supply chain', 'Domestic retail market only', 'Personal baggage process only', 'Stock exchange settlement system', 'Income-tax filing system'], 0, 'AEO - December 2019'),
]

existing = {q['stem'].strip().lower() for q in bank}
for i, (stem, options, correct, source) in enumerate(questions, 1):
    if stem.lower() in existing:
        continue
    bank.append({
        'id': f'cha-source-aeo-{i:02d}',
        'subject': 'allied_acts',
        'source': source,
        'stem': stem,
        'stemHi': stem,
        'options': options,
        'optionsHi': options,
        'correctIndex': correct,
        'explanation': f'Source-based question transcribed and normalised from {source}. Verify current AEO circulars and notifications before relying on any time-sensitive procedural detail.',
        'explanationHi': f'{source} से लिया गया स्रोत-आधारित प्रश्न। समय-संवेदनशील प्रक्रिया के लिए वर्तमान AEO परिपत्र और अधिसूचनाएं भी जांचें।'
    })

path.write_text(json.dumps(bank, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Added source questions. Final count: {len(bank)}')
