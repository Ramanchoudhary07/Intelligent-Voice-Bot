import React from 'react';
import { motion } from 'framer-motion';

const Orb = ({ state }) => {
  // state: 'idle', 'listening', 'processing', 'speaking'
  
  const variants = {
    idle: { scale: 1, opacity: 0.5, rotate: 0 },
    listening: { scale: 1.2, opacity: 0.8, rotate: 0 },
    processing: { scale: [1, 1.1, 1], opacity: 1, rotate: 360, transition: { repeat: Infinity, duration: 2, ease: "linear" } },
    speaking: { scale: [1, 1.3, 1], opacity: 1, rotate: 0, transition: { repeat: Infinity, duration: 1.5 } }
  };

  const colors = {
    idle: 'var(--primary-color)',
    listening: 'var(--accent-color)',
    processing: 'var(--secondary-color)',
    speaking: '#ff0055' // Or another color
  };

  return (
    <div className="relative flex justify-center items-center w-64 h-64">
      {/* Core */}
      <motion.div
        className="absolute w-32 h-32 rounded-full blur-md"
        style={{ backgroundColor: colors[state] }}
        animate={state}
        variants={variants}
      />
      
      {/* Outer Rings */}
      <motion.div
        className="absolute w-48 h-48 rounded-full border-2 border-dashed opacity-30"
        style={{ borderColor: colors[state] }}
        animate={{ rotate: 360 }}
        transition={{ repeat: Infinity, duration: 20, ease: "linear" }}
      />
      
      <motion.div
        className="absolute w-60 h-60 rounded-full border border-opacity-20"
        style={{ borderColor: colors[state] }}
        animate={{ rotate: -360 }}
        transition={{ repeat: Infinity, duration: 15, ease: "linear" }}
      />
      
      {/* Particles/Glow */}
      <div className="absolute w-full h-full rounded-full"
           style={{
             background: `radial-gradient(circle, ${colors[state]}22 0%, transparent 70%)`
           }}
      />
    </div>
  );
};

export default Orb;
