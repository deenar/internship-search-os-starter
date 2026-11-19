// Extraction script for role-finder step 4.
// Substitute the dedup set from data/applications.json into `trackedPairs`.
// Apply category filter from step 2 by adding a category check inside the loop if narrowed.
// Run via javascript_tool in the browser on the Trackr page.

(() => {
  const today = new Date().toISOString().slice(0, 10);
  const in30 = new Date(Date.now() + 30*86400000).toISOString().slice(0,10);
  const trackedPairs = new Set([/* "company|role" lowercase pairs from data/applications.json */]);
  const ineligiblePatterns = /Slovakia|US Citizens Only|Chinese required|Mandarin required|Spanish speakers only|Chemistry|18 months relevant experience|final-year students only/i;
  const quantPattern = /\bquant(itative)?\b/i;

  function parseTrackrDate(s) {
    if (!s) return null;
    const m = s.match(/^(\d{2}) (\w{3}) (\d{2})$/);
    if (!m) return null;
    const months = {Jan:'01',Feb:'02',Mar:'03',Apr:'04',May:'05',Jun:'06',Jul:'07',Aug:'08',Sep:'09',Oct:'10',Nov:'11',Dec:'12'};
    const mm = months[m[2]];
    return mm ? { iso: `20${m[3]}-${mm}-${m[1]}`, dd: m[1], mm, yy: parseInt(m[3], 10) } : null;
  }
  function estimateNextCycle(lastYearStr) {
    const p = parseTrackrDate(lastYearStr);
    return p ? `20${p.yy + 1}-${p.mm}-${p.dd}` : null;
  }

  const table = document.querySelector('table');
  const headers = Array.from(table.querySelectorAll('thead tr th, thead tr td')).map(c => c.textContent.trim());
  const rows = Array.from(table.querySelectorAll('tbody tr'));
  let category = null;
  const results = [];

  for (const r of rows) {
    const cells = Array.from(r.children);
    if (cells.length <= 1) { category = cells[0]?.textContent.trim() || category; continue; }
    const texts = cells.map(c => c.textContent.trim());
    const row = {}; headers.forEach((h, i) => row[h] = texts[i]);
    const company = row['Company Name'], programme = row['Programme Name'];
    if (!company || !programme) continue;
    if (quantPattern.test(programme)) continue;
    const key = `${company.toLowerCase()}|${programme.toLowerCase()}`;
    if (trackedPairs.has(key)) continue;

    const companyLink = cells[1].querySelector('a');
    const openingP = parseTrackrDate(row['Opening Date']);
    const closingP = parseTrackrDate(row['Closing Date']);
    const opening_date = openingP ? openingP.iso : null;
    const closing_date = closingP ? closingP.iso : null;
    const estimated_next_opening = estimateNextCycle(row['Last Year Opening']);

    let bucket;
    if (closing_date && closing_date >= today) bucket = 'upcoming';
    else if (closing_date && closing_date < today) bucket = 'closed';
    else if (opening_date && opening_date <= today) bucket = 'open_rolling_no_deadline';
    else if (estimated_next_opening && estimated_next_opening < today) bucket = 'overdue_vs_last_year';
    else if (estimated_next_opening && estimated_next_opening <= in30) bucket = 'opening_soon';
    else bucket = 'unannounced_later';

    results.push({
      category, company, programme, opening_date, closing_date, bucket,
      last_year_opened: row['Last Year Opening'] || null,
      estimated_next_opening,
      latest_stage: row['Latest Stage'] || null,
      rolling: row['Rolling'] || null,
      process: row['Process'] || null,
      cv_required: row['CV'] || null,
      cover_letter_required: row['Cover Letter'] || null,
      written_answers: row['Written Answers'] || null,
      sponsors_visa: row['Sponsors Visa'] || null,
      notes: row['Notes'] || null,
      possible_ineligible: ineligiblePatterns.test(row['Notes'] || ''),
      trackr_company_url: companyLink ? companyLink.href : null,
    });
  }

  const rank = { upcoming: 0, closed: 1, open_rolling_no_deadline: 2, overdue_vs_last_year: 3, opening_soon: 4, unannounced_later: 5 };
  results.sort((a, b) => {
    const r = rank[a.bucket] - rank[b.bucket];
    if (r !== 0) return r;
    return (a.closing_date || a.estimated_next_opening || '').localeCompare(b.closing_date || b.estimated_next_opening || '') || a.company.localeCompare(b.company);
  });

  const counts = results.reduce((acc, r) => { acc[r.bucket] = (acc[r.bucket] || 0) + 1; return acc; }, {});
  const flaggedIneligible = results.filter(r => r.possible_ineligible);
  return {
    total_untracked: results.length, counts,
    upcoming: results.filter(r => r.bucket === 'upcoming'),
    closed: results.filter(r => r.bucket === 'closed'),
    open_rolling: results.filter(r => r.bucket === 'open_rolling_no_deadline'),
    overdue: results.filter(r => r.bucket === 'overdue_vs_last_year'),
    opening_soon: results.filter(r => r.bucket === 'opening_soon'),
    flaggedIneligible,
  };
})()
