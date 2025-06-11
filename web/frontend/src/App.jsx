import { useState, useEffect } from 'react';
import Questions from './pages/Questions';
import Candidates from './pages/Candidates';
import Tabs from './components/Tabs';
import Timeline from './components/Timeline';

function App() {
  const [activeTab, setActiveTab] = useState('questions');
  const [selectedDate, setSelectedDate] = useState(null);
  const [selectedSource, setSelectedSource] = useState(null);
  const [groupedQuestions, setGroupedQuestions] = useState({});

  useEffect(() => {
    fetch("http://localhost:5001/api/questions/grouped")
      .then(res => res.json())
      .then(data => setGroupedQuestions(data));
  }, []);

  return (
    <div className="app-container" style={{ display: 'flex', height: '100vh' }}>
      <div style={{ width: '280px', borderRight: '1px solid #ccc', padding: '1rem' }}>
        <h2>Timeline</h2>
        <Timeline
          groupedData={groupedQuestions}
          selectedDate={selectedDate}
          selectedSource={selectedSource}
          onSelect={(date, source) => {
            setSelectedDate(date);
            setSelectedSource(source);
          }}
        />
      </div>

      <div style={{ flex: 1, padding: '1rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h2 style={{ margin: 0 }}>
            {activeTab === 'questions' ? 'Questions' : 'Candidates'}
          </h2>
          <button>View Timeline</button>
        </div>

        <Tabs activeTab={activeTab} setActiveTab={setActiveTab} />

        {activeTab === 'questions' ? (
          <Questions selectedDate={selectedDate} selectedSource={selectedSource} />
        ) : (
          <Candidates selectedDate={selectedDate} selectedSource={selectedSource} />
        )}
      </div>
    </div>
  );
}

export default App;
