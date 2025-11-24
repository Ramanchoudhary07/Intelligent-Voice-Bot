import React, { useState, useRef, useEffect } from 'react';
import Orb from '../components/Orb';
import Waveform from '../components/Waveform';
import { Mic, Square, Send } from 'lucide-react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

const Home = () => {
  const [state, setState] = useState('idle'); // idle, listening, processing, speaking
  const [audioStream, setAudioStream] = useState(null);
  const [responseAudio, setResponseAudio] = useState(null);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
  const { user } = useAuth();
  
  // Audio playback
  const audioRef = useRef(new Audio());

  const startListening = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      setAudioStream(stream);
      
      mediaRecorderRef.current = new MediaRecorder(stream);
      chunksRef.current = [];
      
      mediaRecorderRef.current.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data);
        }
      };
      
      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(chunksRef.current, { type: 'audio/wav' }); // or webm
        await processAudio(audioBlob);
        
        // Stop all tracks
        stream.getTracks().forEach(track => track.stop());
        setAudioStream(null);
      };
      
      mediaRecorderRef.current.start();
      setState('listening');
    } catch (err) {
      console.error("Error accessing microphone:", err);
      alert("Could not access microphone");
    }
  };

  const stopListening = () => {
    if (mediaRecorderRef.current && state === 'listening') {
      mediaRecorderRef.current.stop();
      setState('processing');
    }
  };

  const processAudio = async (audioBlob) => {
    const formData = new FormData();
    formData.append('file', audioBlob, 'recording.webm');
    
    try {
      const token = localStorage.getItem('token');
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      
      const response = await axios.post('http://localhost:5000/api/submit_audio', formData, {
        headers: {
          ...headers,
          'Content-Type': 'multipart/form-data'
        }
      });
      
      const { audio_url } = response.data;
      if (audio_url) {
        playResponse(audio_url);
      } else {
        setState('idle');
      }
    } catch (error) {
      console.error("Error processing audio:", error);
      if (error.response) {
          console.error("Server Error:", error.response.status, error.response.data);
          alert(`Error processing audio: ${error.response.data.error || error.response.statusText}`);
      } else {
          alert("Error processing audio: Network Error or Server Unreachable");
      }
      setState('idle');
    }
  };

  const playResponse = (url) => {
    setState('speaking');
    audioRef.current.src = url;
    audioRef.current.play();
    
    audioRef.current.onended = () => {
      setState('idle');
    };
  };

  return (
    <div className="hero-container">
      {/* Background Elements */}
      <div className="absolute inset-0 z-0 pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-[var(--primary-color)] rounded-full mix-blend-screen filter blur-[100px] opacity-10" style={{ filter: 'blur(100px)' }}></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-[var(--secondary-color)] rounded-full mix-blend-screen filter blur-[100px] opacity-10" style={{ filter: 'blur(100px)' }}></div>
        
        {/* Grid Lines */}
        <div className="absolute inset-0" style={{ 
          backgroundImage: 'linear-gradient(rgba(0,243,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(0,243,255,0.03) 1px, transparent 1px)',
          backgroundSize: '40px 40px'
        }}></div>
      </div>

      <div className="z-10 flex flex-col items-center gap-12 w-full max-w-4xl px-4">
        {/* Header/Status */}
        <div className="status-text">
          <h2 className="status-label">SYSTEM STATUS</h2>
          <h1 className="status-value glow-text">{state}</h1>
        </div>

        {/* Main Visualizer */}
        <div className="relative">
          <Orb state={state} />
        </div>

        {/* Waveform (only when listening) */}
        <div className="h-24 w-full flex justify-center items-center">
          {state === 'listening' ? (
            <Waveform audioStream={audioStream} isListening={true} />
          ) : (
             <div className="h-1 w-full max-w-md bg-[var(--glass-border)] rounded-full overflow-hidden">
               {state === 'processing' && (
                 <div className="h-full bg-[var(--primary-color)] w-full" style={{ animation: 'pulse 1s infinite' }}></div>
               )}
             </div>
          )}
        </div>

        {/* Controls */}
        <div className="flex gap-6">
          {state === 'idle' || state === 'speaking' ? (
            <button 
              onClick={startListening}
              className="btn-mic"
            >
              <div className="btn-mic-content">
                <Mic className="w-5 h-5" />
                <span>INITIATE VOICE</span>
              </div>
            </button>
          ) : (
            <button 
              onClick={stopListening}
              className="btn-mic"
              style={{ borderColor: 'red', color: 'red' }}
            >
              <div className="btn-mic-content">
                <Square className="w-5 h-5" />
                <span>TERMINATE</span>
              </div>
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default Home;
