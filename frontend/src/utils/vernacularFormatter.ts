/**
 * Utility functions for Vernacular Formatting across English, Hindi, and Kannada.
 */

const devanagariDigits = ['०', '१', '२', '३', '४', '५', '६', '७', '८', '९'];
const kannadaDigits = ['೦', '೧', '೨', '೩', '೪', '೫', '೬', '೭', '೮', '೯'];

/**
 * Converts Western Arabic numerals (0-9) to Devanagari numerals (०-९) for Hindi or Kannada numerals (೦-೯) for Kannada.
 */
export function formatVernacularNumber(value: number | string | null | undefined, lang: string): string {
  if (value === null || value === undefined || value === '') return '';
  const str = String(value);
  if (lang === 'hi') {
    return str.replace(/\d/g, (d) => devanagariDigits[parseInt(d, 10)]);
  }
  if (lang === 'kn') {
    return str.replace(/\d/g, (d) => kannadaDigits[parseInt(d, 10)]);
  }
  return str;
}

/**
 * Formats a currency value (e.g. ₹2,500) into vernacular numerals and symbol.
 */
export function formatVernacularCurrency(amount: number | string, lang: string): string {
  const num = typeof amount === 'string' ? parseFloat(amount) || 0 : amount;
  const formattedEn = num.toLocaleString('en-IN', { maximumFractionDigits: 1 });
  const vernNumber = formatVernacularNumber(formattedEn, lang);
  return `₹${vernNumber}`;
}

/**
 * Returns localized role label for all account role types.
 */
export function getLocalizedRoleName(roleOrType: string, lang: string): string {
  switch (roleOrType) {
    case 'recycler':
      return lang === 'hi'
        ? 'सत्यापित रीसायकलर (Authorized Recycler)'
        : lang === 'kn'
        ? 'ಅಧಿಕೃತ ಮರುಬಳಕೆದಾರ (Authorized Recycler)'
        : 'Authorized Recycler';
    case 'shop':
      return lang === 'hi'
        ? 'दुकानदार (Shop Owner)'
        : lang === 'kn'
        ? 'ಅಂಗಡಿ ಮಾಲೀಕರು (Shop Owner)'
        : 'Shop Owner';
    case 'sub_collector':
      return lang === 'hi'
        ? 'फेरीवाला (Feriwala Collector)'
        : lang === 'kn'
        ? 'ಫೇರಿವಾಲಾ ಸಂಗ್ರಾಹಕ (Feriwala Collector)'
        : 'Feriwala Collector';
    case 'independent':
    case 'collector':
    default:
      return lang === 'hi'
        ? 'स्वतंत्र कबाड़ीवाला (Independent Collector)'
        : lang === 'kn'
        ? 'ಸ್ವತಂತ್ರ ಗುಜರಿ ಸಂಗ್ರಾಹಕ (Independent Collector)'
        : 'Independent Collector';
  }
}
