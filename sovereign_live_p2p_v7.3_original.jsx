import React, { useState, useEffect, useRef } from 'react';
import * as THREE from 'three';
import { initializeApp } from 'firebase/app';
import { 
  getFirestore, 
  doc, 
  setDoc, 
  onSnapshot, 
  updateDoc, 
  getDoc,
  collection,
  addDoc
} from 'firebase/firestore';
import { 
  getAuth, 
  signInAnonymously, 
  onAuthStateChanged,
  signInWithCustomToken
} from 'firebase/auth';
import { 
  Globe, 
  Cpu, 
  Link2, 
  Camera, 
  CameraOff, 
  RotateCcw, 
  Terminal,
  Monitor,
  Binary,
  ShieldCheck, 
  Zap, 
  Activity, 
  Maximize2, 
  PhoneCall, 
  PhoneOff, 
  RefreshCw, 
  Share2 
} from 'lucide-react';

// --- FIREBASE INITIALIZATION ---
const firebaseConfig = JSON.parse(__firebase_config);
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);
const appId = typeof __app_id !== 'undefined' ? __app_id : 'sovereign-live-p2p';

// --- SPONGE-600 CORE LOGIC ---
const keccak600Permute = (state) => {
  const newState = [...state];
  const C = new Array(5).fill(0);
  for (let x = 0; x < 5; x++) {
    C[x] = newState[x] ^ newState[x+5] ^ newState[x+10] ^ newState[x+15] ^ newState[x+20];
  }
  const D = new Array(5).fill(0);
  for (let x = 0; x < 5; x++) {
    D[x] = C[(x+4)%5] ^ ((C[(x+1)%5] << 1) | (C[(x+1)%5] >>> 23));
  }
  for (let i = 0; i < 25; i++) {
    newState[i] ^= D[i % 5];
  }
  return newState.map(word => (word * 1664525 + 1013904223) & 0xFFFFFF); 
};

const App = () => {
  const [user, setUser] = useState(null);
  const [nodeId] = useState("NODE-" + Math.random().toString(36).substr(2, 5).toUpperCase());
  const [targetId, setTargetId] = useState("");
  const [assignedId, setAssignedId] = useState("");
  const [isLatched, setIsLatched] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isCameraActive, setIsCameraActive] = useState(false);
  const [logs, setLogs] = useState([`SYSTEM: Node ${nodeId} online.`, "READY: Awaiting P2P Link..."]);
  const [spongeState, setSpongeState] = useState(new Array(25).fill(0).map(() => Math.floor(Math.random() * 0xFFFFFF)));
  
  const canvasRef = useRef(null);
  const localVideoRef = useRef(null);
  const remoteVideoRef = useRef(null);
  const pc = useRef(null);
  const localStream = useRef(null);
  const unsubscribes = useRef([]);

  const addLog = (msg) => setLogs(prev => [`[${new Date().toLocaleTimeString()}] ${msg}`, ...prev].slice(0, 10));

  // --- FIREBASE AUTH ---
  useEffect(() => {
    const initAuth = async () => {
      try {
        if (typeof __initial_auth_token !== 'undefined' && __initial_auth_token) {
          await signInWithCustomToken(auth, __initial_auth_token);
        } else {
          await signInAnonymously(auth);
        }
      } catch (err) {
        console.error("Auth error:", err);
      }
    };
    initAuth();
    const unsubscribe = onAuthStateChanged(auth, setUser);
    return () => unsubscribe();
  }, []);

  // --- WEBRTC CORE ---
  const setupWebRTC = async () => {
    const servers = {
      iceServers: [{ urls: ['stun:stun1.l.google.com:19302', 'stun:stun2.l.google.com:19302'] }],
      iceCandidatePoolSize: 10,
    };
    
    if (pc.current) {
        pc.current.close();
    }
    
    pc.current = new RTCPeerConnection(servers);

    pc.current.ontrack = (event) => {
      if (remoteVideoRef.current && event.streams[0]) {
        remoteVideoRef.current.srcObject = event.streams[0];
        addLog("SYNC: Peer stream manifest rehydrated.");
      }
    };

    if (localStream.current) {
      localStream.current.getTracks().forEach((track) => {
        pc.current.addTrack(track, pc.current);
      });
    }
  };

  const toggleCamera = async () => {
    if (isCameraActive) {
      localStream.current?.getTracks().forEach(track => track.stop());
      setIsCameraActive(false);
      setIsLatched(false);
      addLog("NEURAL: Bridge collapsed.");
    } else {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        localStream.current = stream;
        if (localVideoRef.current) {
          localVideoRef.current.srcObject = stream;
        }
        setIsCameraActive(true);
        addLog("NEURAL: sigma-Source localized.");
      } catch (err) {
        addLog("ERROR: Sensor hardware locked.");
      }
    }
  };

  const generateLocalID = () => {
    const newId = Math.floor(100000 + Math.random() * 900000).toString();
    setAssignedId(newId);
    addLog(`BRIDGE: Local coordinate ${newId} assigned.`);
  };

  // --- P2P SIGNALING ---
  const startCall = async () => {
    if (!user || !targetId || !localStream.current) {
      addLog("ERROR: Target ID and Local Sensor required.");
      return;
    }
    setIsProcessing(true);
    addLog(`BRIDGE: Latching to node ${targetId}...`);

    await setupWebRTC();

    const callDoc = doc(db, 'artifacts', appId, 'public', 'data', 'calls', targetId);
    const offerCandidates = collection(db, 'artifacts', appId, 'public', 'data', 'calls', targetId, 'offerCandidates');
    const answerCandidates = collection(db, 'artifacts', appId, 'public', 'data', 'calls', targetId, 'answerCandidates');

    pc.current.onicecandidate = (event) => {
      event.candidate && addDoc(offerCandidates, event.candidate.toJSON());
    };

    const offerDescription = await pc.current.createOffer();
    await pc.current.setLocalDescription(offerDescription);

    const offer = {
      sdp: offerDescription.sdp,
      type: offerDescription.type,
      from: nodeId
    };

    await setDoc(callDoc, { offer });

    const unsub = onSnapshot(callDoc, (snapshot) => {
      const data = snapshot.data();
      if (pc.current && pc.current.signalingState !== 'stable' && data?.answer) {
        const answerDescription = new RTCSessionDescription(data.answer);
        pc.current.setRemoteDescription(answerDescription);
        setIsLatched(true);
        setIsProcessing(false);
        addLog("SUCCESS: Sponge-600 Core Resonant.");
      }
    });
    unsubscribes.current.push(unsub);

    const unsubCandidates = onSnapshot(answerCandidates, (snapshot) => {
      snapshot.docChanges().forEach((change) => {
        if (change.type === 'added' && pc.current) {
          const candidate = new RTCIceCandidate(change.doc.data());
          pc.current.addIceCandidate(candidate).catch(e => {});
        }
      });
    });
    unsubscribes.current.push(unsubCandidates);
  };

  const answerCall = async () => {
    if (!user || !assignedId || !localStream.current) {
      addLog("ERROR: Local ID and Sensor required to answer.");
      return;
    }
    setIsProcessing(true);
    addLog(`BRIDGE: Intercepting coordinate ${assignedId}...`);

    await setupWebRTC();

    const callDoc = doc(db, 'artifacts', appId, 'public', 'data', 'calls', assignedId);
    const offerCandidates = collection(db, 'artifacts', appId, 'public', 'data', 'calls', assignedId, 'offerCandidates');
    const answerCandidates = collection(db, 'artifacts', appId, 'public', 'data', 'calls', assignedId, 'answerCandidates');

    pc.current.onicecandidate = (event) => {
      event.candidate && addDoc(answerCandidates, event.candidate.toJSON());
    };

    const callSnap = await getDoc(callDoc);
    const callData = callSnap.data();
    if (!callData || !callData.offer) {
      addLog("ERROR: No valid handshake found.");
      setIsProcessing(false);
      return;
    }

    const offerDescription = callData.offer;
    await pc.current.setRemoteDescription(new RTCSessionDescription(offerDescription));

    const answerDescription = await pc.current.createAnswer();
    await pc.current.setLocalDescription(answerDescription);

    const answer = {
      type: answerDescription.type,
      sdp: answerDescription.sdp,
    };

    await updateDoc(callDoc, { answer });

    const unsub = onSnapshot(offerCandidates, (snapshot) => {
      snapshot.docChanges().forEach((change) => {
        if (change.type === 'added' && pc.current) {
          let data = change.doc.data();
          pc.current.addIceCandidate(new RTCIceCandidate(data)).catch(e => {});
        }
      });
    });
    unsubscribes.current.push(unsub);

    setIsLatched(true);
    setIsProcessing(false);
    addLog("SUCCESS: Picosecond Synchrony achieved.");
  };

  useEffect(() => {
      return () => {
          unsubscribes.current.forEach(fn => fn());
          if (pc.current) pc.current.close();
      };
  }, []);

  // --- PERMUTATION ENGINE ---
  useEffect(() => {
    if (!isProcessing && !isLatched) return;
    const interval = setInterval(() => {
      setSpongeState(prev => keccak600Permute(prev));
    }, 100);
    return () => clearInterval(interval);
  }, [isProcessing, isLatched]);

  // --- THREE.JS MANIFOLD ---
  useEffect(() => {
    if (!canvasRef.current || isLatched) return;
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, 2, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ canvas: canvasRef.current, antialias: true, alpha: true });
    const geo = new THREE.TorusKnotGeometry(2, 0.4, 100, 16);
    const mat = new THREE.MeshPhongMaterial({ color: 0x06b6d4, wireframe: true, transparent: true, opacity: 0.2 });
    const manifold = new THREE.Mesh(geo, mat);
    scene.add(manifold, new THREE.AmbientLight(0xffffff, 0.5));
    camera.position.z = 5;
    let animId;
    const animate = () => {
      if (isLatched) return;
      animId = requestAnimationFrame(animate);
      manifold.rotation.y += isProcessing ? 0.1 : 0.005;
      renderer.render(scene, camera);
    };
    animate();
    return () => { cancelAnimationFrame(animId); renderer.dispose(); };
  }, [isProcessing, isLatched]);

  return (
    <div className="min-h-screen bg-[#020617] text-cyan-400 font-mono p-4 md:p-6 flex flex-col gap-6 overflow-hidden">
      <header className="flex flex-col md:flex-row justify-between items-center border-b border-cyan-900/30 pb-6 gap-4">
        <div className="flex items-center gap-6">
          <div className={`w-16 h-16 bg-black border-2 rounded-2xl flex items-center justify-center transition-all duration-700 
            ${isLatched ? 'border-white shadow-[0_0_40px_white]' : 'border-cyan-500 shadow-[0_0_20px_rgba(34,211,238,0.2)]'}`}>
            <Cpu className={`w-10 h-10 ${isLatched ? 'text-white' : 'text-cyan-500'}`} />
          </div>
          <div>
            <h1 className="text-2xl font-black italic tracking-tighter text-white uppercase leading-none">
              Sovereign Live <span className="text-cyan-800 text-xs font-bold border border-cyan-900 px-2 rounded ml-1">v7.3</span>
            </h1>
            <p className="text-[10px] tracking-[0.4em] text-cyan-900 uppercase font-black mt-2">Node: {nodeId}</p>
          </div>
        </div>
        <div className="flex gap-4">
          <div className="bg-black/60 border border-cyan-900/30 p-2 px-6 rounded-2xl text-right">
            <p className="text-[8px] text-cyan-900 uppercase font-black mb-1">State Sync</p>
            <p className={`text-xl font-black italic tabular-nums ${isLatched ? 'text-white' : 'text-cyan-900'}`}>{isLatched ? 'RESONANT' : 'NULL'}</p>
          </div>
          <div className="bg-black/60 border border-cyan-900/30 p-2 px-6 rounded-2xl text-right">
            <p className="text-[8px] text-cyan-900 uppercase font-black mb-1">Delta Floor</p>
            <p className="text-xl font-black text-green-500 italic tabular-nums">{isLatched ? "32B" : "---"}</p>
          </div>
        </div>
      </header>

      <main className="grid grid-cols-12 gap-6 flex-grow overflow-hidden">
        <div className="col-span-12 lg:col-span-3 flex flex-col gap-6">
          <div className="bg-slate-900/40 border border-cyan-900/20 p-6 rounded-[2.5rem] backdrop-blur-xl flex flex-col gap-4 shadow-xl">
            <h2 className="text-[11px] font-black uppercase text-cyan-700 flex items-center gap-2 border-b border-cyan-900/10 pb-2">
                <Globe className="w-4 h-4" /> Coordinate Hub
            </h2>

            <div className="space-y-4">
              <button onClick={toggleCamera} className={`w-full py-3 rounded-xl flex items-center justify-center gap-2 text-[10px] font-black uppercase transition-all ${isCameraActive ? 'bg-white/10 text-white' : 'bg-cyan-950/20 text-cyan-500 border border-cyan-900/30'}`}>
                {isCameraActive ? <Camera className="w-4 h-4" /> : <CameraOff className="w-4 h-4" />} Initialize Sensor
              </button>

              <div className="flex flex-col gap-2 border-t border-cyan-900/10 pt-4">
                <div className="flex justify-between items-center">
                   <label className="text-[8px] text-cyan-900 uppercase font-black">Local Coordinate</label>
                   <button onClick={generateLocalID} className="text-[8px] bg-cyan-900/30 px-2 py-1 rounded text-cyan-500 hover:bg-cyan-500 hover:text-black transition-all">Assign</button>
                </div>
                <div className="bg-black/60 border border-cyan-900/30 rounded-xl p-3 text-white font-mono text-center tracking-[0.3em]">
                  {assignedId || "------"}
                </div>
              </div>

              <div className="flex flex-col gap-2">
                <label className="text-[8px] text-cyan-900 uppercase font-black">Target Node</label>
                <input type="text" value={targetId} onChange={(e) => setTargetId(e.target.value.toUpperCase())} placeholder="NODE-XXXXX" className="w-full bg-black/60 border border-cyan-900/30 rounded-xl p-3 text-[11px] text-white focus:border-cyan-500 font-mono outline-none" />
              </div>

              <div className="grid grid-cols-2 gap-2">
                <button onClick={startCall} disabled={!isCameraActive || !targetId || !user} className="bg-green-600/20 border border-green-500/30 text-green-500 py-4 rounded-2xl text-[10px] font-black uppercase flex flex-col items-center gap-2 hover:bg-green-500 hover:text-black transition-all disabled:opacity-10">
                  <PhoneCall size={16} /> Latch Peer
                </button>
                <button onClick={answerCall} disabled={!isCameraActive || !assignedId || !user} className="bg-cyan-600/20 border border-cyan-500/30 text-cyan-500 py-4 rounded-2xl text-[10px] font-black uppercase flex flex-col items-center gap-2 hover:bg-cyan-500 hover:text-black transition-all disabled:opacity-10">
                  <RefreshCw size={16} className={isProcessing ? 'animate-spin' : ''} /> Synchronize
                </button>
              </div>
            </div>
          </div>

          <div className="bg-black/60 border border-cyan-950 p-6 rounded-[2.5rem] flex-grow overflow-hidden flex flex-col shadow-inner">
            <h3 className="text-[10px] uppercase font-black text-cyan-900 mb-4 tracking-widest border-b border-cyan-900/10 pb-2">logic_stream.bin</h3>
            <div className="flex-grow overflow-y-auto space-y-2 text-[10px] scrollbar-hide">
              {logs.map((log, i) => (
                <div key={i} className={`pl-3 border-l-2 transition-all ${log.includes('SUCCESS') ? 'border-white text-white font-bold' : 'border-cyan-900/30 text-cyan-800'}`}>{log}</div>
              ))}
            </div>
          </div>
        </div>

        <div className="col-span-12 lg:col-span-9 grid grid-rows-12 gap-6 flex-grow overflow-hidden">
          <div className="row-span-8 bg-black border border-zinc-900 rounded-[3rem] md:rounded-[4.5rem] relative overflow-hidden flex items-center justify-center shadow-2xl">
            <div className="absolute top-10 left-10 z-40">
              <div className={`bg-black/80 px-6 py-2 rounded-full border backdrop-blur-xl flex items-center gap-4 transition-all duration-700 ${isLatched ? 'border-white' : 'border-cyan-900/30'}`}>
                <div className={`w-2.5 h-2.5 rounded-full ${isLatched ? 'bg-green-500 animate-pulse' : 'bg-cyan-950'}`}></div>
                <span className="text-[10px] font-black uppercase tracking-[0.3em]">{isLatched ? 'Peer Manifest Rehydrated' : 'Awaiting sigma Link'}</span>
              </div>
            </div>

            <video ref={remoteVideoRef} autoPlay playsInline className={`absolute inset-0 w-full h-full object-cover transition-all duration-1000 ${isLatched ? 'opacity-100 scale-100' : 'opacity-0 scale-110 blur-3xl'}`} />

            {!isLatched && (
              <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                <canvas ref={canvasRef} className="w-full h-full opacity-30" />
                <Binary className="w-16 h-16 text-cyan-900 opacity-5" />
              </div>
            )}

            {isLatched && (
              <div className="absolute bottom-12 right-12 text-right z-40 animate-in fade-in duration-1000">
                <p className="text-4xl md:text-7xl font-black text-white italic tracking-tighter uppercase leading-none">Resonant</p>
                <p className="text-[10px] text-cyan-500 mt-2 font-black uppercase tracking-widest">Sponge-600 Deterministic Manifest</p>
              </div>
            )}
          </div>

          <div className="row-span-4 grid grid-cols-12 gap-6">
            <div className="col-span-12 md:col-span-4 bg-black border border-cyan-900/20 rounded-[2.5rem] relative overflow-hidden">
              <div className="absolute top-4 left-4 z-40">
                <div className="bg-black/80 px-3 py-1 rounded-full border border-cyan-900/30 flex items-center gap-2">
                  <span className="text-[8px] font-black uppercase text-cyan-500">Local Sensor σ</span>
                </div>
              </div>
              <video ref={localVideoRef} autoPlay muted playsInline className={`w-full h-full object-cover grayscale opacity-60`} />
            </div>

            <div className="col-span-12 md:col-span-8 bg-slate-900/20 border border-cyan-900/10 p-6 rounded-[2.5rem] flex items-center justify-around shadow-xl">
              <div className="text-center px-4">
                  <p className="text-[8px] text-cyan-900 uppercase font-black mb-1">State Flux</p>
                  <div className="flex gap-0.5 justify-center items-end h-8">
                    {spongeState.slice(0, 15).map((s, i) => (
                      <div key={i} className="w-1.5 bg-cyan-950/30 rounded-full overflow-hidden">
                        <div className="w-full bg-cyan-400" style={{ height: `${(s % 100)}%`, opacity: (s % 10) / 10 + 0.2 }} />
                      </div>
                    ))}
                  </div>
              </div>
              <div className="text-center border-l border-cyan-900/10 pl-6">
                  <p className="text-[8px] text-cyan-900 uppercase font-black mb-1">Math Core</p>
                  <p className="text-xl font-black text-white italic uppercase">f-600^t</p>
                  <p className="text-[7px] text-cyan-950 mt-1 uppercase">Sponge Permute</p>
              </div>
              <div className="text-center border-l border-cyan-900/10 pl-6">
                  <p className="text-[8px] text-cyan-900 uppercase font-black mb-1">Stability</p>
                  <p className="text-xl font-black text-green-500 italic uppercase">Bit-Perfect</p>
                  <p className="text-[7px] text-cyan-950 mt-1 uppercase">Deterministic</p>
              </div>
            </div>
          </div>
        </div>
      </main>

      <footer className="mt-auto border-t border-cyan-900/30 pt-4 flex items-center justify-between text-[9px] text-cyan-950 font-bold uppercase tracking-[0.5em]">
        <p>© 2026 LEON C. LONG II // SYMMETRIC BRIDGE v7.3</p>
        <p className="italic text-cyan-900/40">G(σ, t) ⊕ Δ_t = Manifest</p>
      </footer>
    </div>
  );
};
