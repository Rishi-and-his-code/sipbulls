import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "cha_questions.json"


def q(qid, subject, source, stem, options, correct, explanation, stem_hi, options_hi, explanation_hi):
    return {
        "id": qid,
        "subject": subject,
        "source": source,
        "stem": stem,
        "stemHi": stem_hi,
        "options": options,
        "optionsHi": options_hi,
        "correctIndex": correct,
        "explanation": explanation,
        "explanationHi": explanation_hi,
    }


# These records are the genuinely distinct, source-based facts retained from the
# historical 350/500-question revisions. The large templated batches from those
# revisions are intentionally not restored: they repeated the same fact with
# cosmetic wording changes.
ADDITIONS = [
    q(
        "cha-aeo-176",
        "allied_acts",
        "AEO - December 2019",
        "In which year was the WCO SAFE Framework of Standards adopted?",
        ["2003", "2004", "2005", "2006"],
        2,
        "The World Customs Organization adopted the SAFE Framework of Standards in 2005.",
        "WCO SAFE फ्रेमवर्क ऑफ स्टैंडर्ड्स को किस वर्ष अपनाया गया था?",
        ["2003", "2004", "2005", "2006"],
        "विश्व सीमा शुल्क संगठन ने SAFE फ्रेमवर्क ऑफ स्टैंडर्ड्स को 2005 में अपनाया था।",
    ),
    q(
        "cha-aeo-177",
        "allied_acts",
        "AEO - December 2019",
        "The WCO SAFE Framework of Standards deals with supply-chain management through which transport modes?",
        ["Air only", "Road only", "Sea only", "All modes of transport"],
        3,
        "The SAFE Framework is designed for international supply chains across all modes of transport, not only one mode.",
        "WCO SAFE फ्रेमवर्क ऑफ स्टैंडर्ड्स किन परिवहन माध्यमों के जरिए सप्लाई-चेन प्रबंधन से संबंधित है?",
        ["केवल हवाई परिवहन", "केवल सड़क परिवहन", "केवल समुद्री परिवहन", "सभी परिवहन माध्यम"],
        "SAFE फ्रेमवर्क केवल एक माध्यम तक सीमित नहीं है; यह सभी परिवहन माध्यमों वाली अंतरराष्ट्रीय सप्लाई चेन के लिए बनाया गया है।",
    ),
    q(
        "cha-aeo-178",
        "allied_acts",
        "AEO - December 2019",
        "Which is a core element of the WCO SAFE Framework of Standards?",
        ["Advance electronic information about inbound, outbound and transit shipments", "Removal of risk management", "A ban on electronic filing", "Elimination of Customs-to-Business cooperation"],
        0,
        "Advance electronic information about inbound, outbound and transit shipments is a core SAFE Framework element supporting risk assessment and supply-chain security.",
        "WCO SAFE फ्रेमवर्क ऑफ स्टैंडर्ड्स का मुख्य तत्व कौन सा है?",
        ["आने वाली, बाहर जाने वाली और ट्रांजिट खेपों की अग्रिम इलेक्ट्रॉनिक जानकारी", "जोखिम प्रबंधन को हटाना", "इलेक्ट्रॉनिक फाइलिंग पर प्रतिबंध", "सीमा शुल्क और व्यवसाय के बीच सहयोग समाप्त करना"],
        "आने वाली, बाहर जाने वाली और ट्रांजिट खेपों की अग्रिम इलेक्ट्रॉनिक जानकारी SAFE फ्रेमवर्क का मुख्य तत्व है, जो जोखिम आकलन और सप्लाई-चेन सुरक्षा में सहायता करती है।",
    ),
    q(
        "cha-aeo-179",
        "allied_acts",
        "AEO - December 2019",
        "Who grants Authorized Economic Operator status in a country?",
        ["World Customs Organization", "The national Customs administration", "A trade chamber alone", "The carrier"],
        1,
        "AEO status is granted by the national Customs administration under that country's applicable programme and criteria.",
        "किसी देश में अधिकृत आर्थिक ऑपरेटर (AEO) का दर्जा कौन प्रदान करता है?",
        ["विश्व सीमा शुल्क संगठन", "राष्ट्रीय सीमा शुल्क प्रशासन", "केवल व्यापार मंडल", "परिवहनकर्ता"],
        "AEO का दर्जा उस देश के लागू कार्यक्रम और मानदंडों के अनुसार राष्ट्रीय सीमा शुल्क प्रशासन प्रदान करता है।",
    ),
    q(
        "cha-aeo-180",
        "allied_acts",
        "AEO - December 2019",
        "In the AEO study material, what does ISCM stand for?",
        ["Integrated Supply Chain Management", "International Customs Security Method", "Internal Statutory Compliance Manual", "Import Supply Clearance Mechanism"],
        0,
        "ISCM stands for Integrated Supply Chain Management in the referenced AEO study material.",
        "AEO अध्ययन सामग्री में ISCM का पूरा नाम क्या है?",
        ["इंटीग्रेटेड सप्लाई चेन मैनेजमेंट", "इंटरनेशनल कस्टम्स सिक्योरिटी मेथड", "इंटरनल स्टैच्यूटरी कंप्लायंस मैनुअल", "इंपोर्ट सप्लाई क्लीयरेंस मैकेनिज्म"],
        "संदर्भित AEO अध्ययन सामग्री में ISCM का अर्थ Integrated Supply Chain Management यानी इंटीग्रेटेड सप्लाई चेन मैनेजमेंट है।",
    ),
    q(
        "cha-aeo-181",
        "allied_acts",
        "AEO - December 2019",
        "The AEO programme is intended to improve Customs capability to do what?",
        ["Detect high-risk consignments", "Eliminate every risk from international trade", "Stop all imports", "Replace all Customs officers"],
        0,
        "The AEO and SAFE approach helps Customs focus resources and improve the detection of high-risk consignments while facilitating legitimate trade.",
        "AEO कार्यक्रम का उद्देश्य सीमा शुल्क की किस क्षमता में सुधार करना है?",
        ["उच्च जोखिम वाली खेपों का पता लगाना", "अंतरराष्ट्रीय व्यापार के हर जोखिम को समाप्त करना", "सभी आयात रोकना", "सभी सीमा शुल्क अधिकारियों का स्थान लेना"],
        "AEO और SAFE दृष्टिकोण वैध व्यापार को सुविधा देते हुए संसाधनों को केंद्रित करने तथा उच्च जोखिम वाली खेपों का पता लगाने में सीमा शुल्क की क्षमता बढ़ाते हैं।",
    ),
    q(
        "cha-aeo-182",
        "allied_acts",
        "AEO - December 2019",
        "The SAFE Framework is primarily concerned with security and facilitation of which supply chain?",
        ["The international supply chain", "Only the domestic retail chain", "Only passenger baggage", "Only the stock-market settlement chain"],
        0,
        "The SAFE Framework addresses security and facilitation of the international supply chain.",
        "SAFE फ्रेमवर्क मुख्य रूप से किस सप्लाई चेन की सुरक्षा और सुविधा से संबंधित है?",
        ["अंतरराष्ट्रीय सप्लाई चेन", "केवल घरेलू खुदरा सप्लाई चेन", "केवल यात्री सामान", "केवल शेयर बाजार की निपटान चेन"],
        "SAFE फ्रेमवर्क अंतरराष्ट्रीय सप्लाई चेन की सुरक्षा और सुविधा से संबंधित है।",
    ),
    q(
        "cha-aeo-183",
        "allied_acts",
        "AEO - December 2019",
        "Which document is not normally identified as an AEO applicant security or process document in the referenced material?",
        ["Security plan", "Site plan", "Process map", "Business plan"],
        3,
        "The referenced AEO material identifies security and process documents such as a security plan, site plan, process map and self-assessment material; a business plan is not the listed security/process document in that context.",
        "संदर्भित सामग्री में AEO आवेदक के सुरक्षा या प्रक्रिया संबंधी दस्तावेज के रूप में किस दस्तावेज की सामान्यतः पहचान नहीं की जाती?",
        ["सुरक्षा योजना", "साइट योजना", "प्रक्रिया मानचित्र", "व्यवसाय योजना"],
        "संदर्भित AEO सामग्री में सुरक्षा योजना, साइट योजना, प्रक्रिया मानचित्र और स्व-मूल्यांकन सामग्री जैसे दस्तावेज बताए गए हैं; उस संदर्भ में व्यवसाय योजना सूचीबद्ध सुरक्षा या प्रक्रिया दस्तावेज नहीं है।",
    ),
    q(
        "cha-aeo-184",
        "allied_acts",
        "AEO - December 2019",
        "Which of the following best describes an AEO benefit where the applicable programme provides it?",
        ["Reduced bank guarantee or equivalent financial-security requirement", "Automatic exemption from every Customs law", "Permission to stop maintaining records", "Permission to conceal shipment information"],
        0,
        "AEO programmes may provide reduced bank-guarantee or equivalent financial-security requirements, but only subject to the applicable programme conditions; AEO status does not exempt a business from Customs law or records duties.",
        "जहाँ लागू कार्यक्रम में प्रावधान हो, निम्नलिखित में से कौन सा AEO लाभ का सबसे अच्छा वर्णन है?",
        ["बैंक गारंटी या समान वित्तीय सुरक्षा की आवश्यकता में कमी", "हर सीमा शुल्क कानून से स्वतः छूट", "रिकॉर्ड रखना बंद करने की अनुमति", "खेप की जानकारी छिपाने की अनुमति"],
        "AEO कार्यक्रम में लागू शर्तों के अधीन बैंक गारंटी या समान वित्तीय सुरक्षा की आवश्यकता में कमी का लाभ मिल सकता है; AEO दर्जा सीमा शुल्क कानून या रिकॉर्ड रखने के दायित्व से छूट नहीं देता।",
    ),
    q(
        "cha-act-185",
        "customs_act",
        "Customs Act 1962",
        "Which chapter of the Customs Act, 1962 contains the provisions on advance rulings?",
        ["Chapter IV", "Chapter V-A", "Chapter V-B", "Chapter VI"],
        2,
        "The advance-ruling provisions are contained in Chapter V-B of the Customs Act, 1962, including Sections 28E to 28M as applicable to the statutory framework.",
        "सीमा शुल्क अधिनियम, 1962 के किस अध्याय में अग्रिम निर्णय से संबंधित प्रावधान हैं?",
        ["अध्याय IV", "अध्याय V-A", "अध्याय V-B", "अध्याय VI"],
        "सीमा शुल्क अधिनियम, 1962 में अग्रिम निर्णय से संबंधित प्रावधान अध्याय V-B में हैं, जिसमें लागू वैधानिक ढांचे के अनुसार धारा 28E से 28M शामिल हैं।",
    ),
]

bank = json.loads(DATA.read_text(encoding="utf-8"))
existing_ids = {item["id"] for item in bank}
for item in ADDITIONS:
    if item["id"] not in existing_ids:
        bank.append(item)
        existing_ids.add(item["id"])

DATA.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"CHA bank now contains {len(bank)} records")
