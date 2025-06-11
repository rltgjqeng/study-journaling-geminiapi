// src/pages/Candidates.jsx
/*import { useEffect, useState } from 'react';
import CandidateCard from '../components/CandidateCard';

function Candidates() {
  const [groupedCandidates, setGroupedCandidates] = useState({});

  useEffect(() => {
    fetch('http://localhost:5001/api/question_candidates/grouped')
      .then(res => res.json())
      .then(data => {
        console.log("후보 데이터:", data);
        setGroupedCandidates(data);
      });
  }, []);

  return (
    <div>
      {Object.entries(groupedCandidates).map(([date, sources]) => (
        <div key={date}>
          <h3 style={{ marginTop: '1rem', color: '#367588' }}>{date}</h3>
          {Object.entries(sources).map(([source, candidates]) => (
            <div key={source} style={{ marginLeft: '1rem' }}>
              <h4>{source}</h4>
              {candidates.map(c => (
                <CandidateCard key={c.id} candidate={c} />
              ))}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}

export default Candidates;*/
// src/pages/Candidates.jsx
import { useEffect, useState } from 'react';
import CandidateCard from '../components/CandidateCard';

function Candidates({ selectedDate, selectedSource }) {
  const [groupedCandidates, setGroupedCandidates] = useState({});

  useEffect(() => {
    fetch('http://localhost:5001/api/question_candidates/grouped')
      .then(res => res.json())
      .then(data => setGroupedCandidates(data));
  }, []);

  if (!selectedDate || !selectedSource) {
    return <div style={{ color: '#888' }}>좌측 타임라인에서 날짜와 출처를 선택해주세요.</div>;
  }

  const candidatesToShow = groupedCandidates?.[selectedDate]?.[selectedSource] || [];

  const sorted = [...candidatesToShow].sort(
    (a, b) => new Date(a.timestamp) - new Date(b.timestamp)
  );

  return (
    <div>
      {sorted.map((c) => (
        <CandidateCard key={c.id} candidate={c} />
      ))}
    </div>
  );
}

export default Candidates;