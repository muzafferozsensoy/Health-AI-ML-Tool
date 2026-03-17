import { apiGet } from './client';

const DOMAIN_MAP = {
  cardiology: 'cardiology',
  radiology: 'radiology',
  nephrology: 'nephrology',
  oncology: 'oncology',
  neurology: 'neurology',
  endocrinology: 'endocrinology',
  pulmonology: 'pulmonology',
  dermatology: 'dermatology',
  ophthalmology: 'ophthalmology',
  gastroenterology: 'gastroenterology',
  hepatology: 'gastroenterology',
  'mental-health': 'psychiatry',
  diabetes: 'endocrinology',
  'sepsis-icu': 'paediatrics',
  'fetal-health': 'obstetrics',
  stroke: 'neurology',
  'cardiology-stroke': 'neurology',
  orthopedics: 'orthopaedics',
  hematology: 'haematology',
  'infectious-disease': 'infectious_disease',
};

export async function fetchClinicalContext(domainId) {
  const backendKey = DOMAIN_MAP[domainId];
  if (!backendKey) return { data: null, error: 'No backend mapping for this domain.' };
  return apiGet(`/step1/context/${backendKey}`);
}
