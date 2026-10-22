const SITE = 'https://sipbulls.com';

export const seoPages = {
  home: {
    title: 'Free NISM V-D & CHA Exam Preparation | SIPBULLS',
    description: 'Free NISM Series V-D and CHA / CBLR exam preparation with question banks, study notes, bilingual explanations and mock tests.',
    keywords: ['NISM V-D preparation', 'NISM Series V-D mock test', 'NISM question bank', 'CHA exam preparation', 'CBLR exam preparation', 'free CHA questions', 'free exam material']
  },
  cha: {
    title: 'CHA / CBLR Exam Preparation: Free Study Notes & Material | SIPBULLS',
    description: 'Prepare for the Customs Broker License Examination with free bilingual CHA study notes, Customs Act summaries, CBLR 2018 concepts and mock-test practice.',
    keywords: ['CHA exam preparation', 'Custom House Agent exam', 'Customs Broker exam', 'CBLR 2018 notes', 'Customs Act 1962 notes', 'free CHA study material']
  },
  chaBank: {
    title: 'Free CHA Exam Questions & CBLR Question Bank | SIPBULLS',
    description: 'Practise free CHA and CBLR exam questions with answers and explanations covering Customs Act 1962, CBLR 2018, valuation, warehousing, baggage and procedures.',
    keywords: ['free CHA questions', 'CHA question bank', 'CBLR question bank', 'Customs Broker MCQs', 'Customs Act MCQs with answers', 'CHA practice questions']
  },
  chaExam: {
    title: 'Free CHA / CBLR Mock Test Online | SIPBULLS',
    description: 'Take a free CHA / CBLR mock test online with randomized exam questions, 150-question CBT practice, +3/-1 marking and detailed answer review.',
    keywords: ['CHA mock test', 'CBLR mock test online', 'Customs Broker mock test', 'CHA exam test series', 'free CBLR practice test']
  },
  notes: {
    title: 'CHA Exam Notes: Customs Act & CBLR 2018 Study Guide | SIPBULLS',
    description: 'Free CHA exam notes and CBLR 2018 study material covering Customs Act 1962, customs procedures and allied topics in English and Hindi.',
    keywords: ['CHA exam notes', 'CBLR 2018 study material', 'Customs Act 1962 notes', 'Custom House Agent notes', 'free customs study material']
  },
  nismBank: {
    title: 'Free NISM Series V-D Question Bank with Answers | SIPBULLS',
    description: 'Practise NISM Series V-D questions with answers and explanations for Specialized Investment Fund Distributors certification preparation.',
    keywords: ['NISM V-D question bank', 'NISM V-D questions with answers', 'NISM mock questions', 'free NISM study material', 'Specialized Investment Fund exam']
  },
  nismExam: {
    title: 'Free NISM Series V-D Mock Test Online | SIPBULLS',
    description: 'Take a free NISM Series V-D mock test online with timed practice, exam-style questions, score tracking and answer explanations.',
    keywords: ['NISM V-D mock test', 'NISM Series V-D online test', 'NISM exam practice', 'NISM V-D test series', 'free NISM mock exam']
  }
};

export function canonical(path = '') {
  return `${SITE}/${path}`;
}
