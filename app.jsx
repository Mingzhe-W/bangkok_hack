// App.jsx
import React, { useState, useEffect, useRef } from 'react';
import * as THREE from 'three';
import { VRButton } from 'three/examples/jsm/webxr/VRButton';

const App = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const sceneRef = useRef(null);

  useEffect(() => {
    // 初始化 Three.js 场景
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.xr.enabled = true;
    document.body.appendChild(renderer.domElement);
    document.body.appendChild(VRButton.createButton(renderer));

    // 炫酷阿米巴虚拟形象
    const geometry = new THREE.SphereGeometry(5, 64, 64);
    const material = new THREE.ShaderMaterial({
      uniforms: {
        time: { value: 1.0 },
        color: { value: new THREE.Color(0x00ffcc) },
      },
      vertexShader: `
        varying vec3 vNormal;
        void main() {
          vNormal = normalize(normal);
          gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
      `,
      fragmentShader: `
        uniform vec3 color;
        varying vec3 vNormal;
        void main() {
          gl_FragColor = vec4(color * abs(vNormal), 1.0);
        }
      `,
    });
    const amiba = new THREE.Mesh(geometry, material);
    scene.add(amiba);

    camera.position.z = 15;

    const animate = () => {
      requestAnimationFrame(animate);
      material.uniforms.time.value += 0.05;
      amiba.rotation.y += 0.01;
      renderer.render(scene, camera);
    };

    animate();
    sceneRef.current = { scene, camera, renderer, amiba };
  }, []);

  const startRecording = () => {
    setIsRecording(true);
    // 语音录制逻辑
    navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
      const mediaRecorder = new MediaRecorder(stream);
      const audioChunks = [];
      mediaRecorder.ondataavailable = (event) => audioChunks.push(event.data);
      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        setAudioBlob(audioBlob);
        stream.getTracks().forEach((track) => track.stop());
      };
      mediaRecorder.start();
      setTimeout(() => mediaRecorder.stop(), 5000); // 录制 5 秒
    });
  };

  const sendToBackend = async () => {
    if (audioBlob) {
      const formData = new FormData();
      formData.append('audio', audioBlob, 'input.wav');
      const response = await fetch('/api/ai-input', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      console.log(data); // AI 的回复
    }
  };

  return (
    <div>
      <button onClick={startRecording} className="btn btn-primary">
        {isRecording ? 'Recording...' : 'Start Recording'}
      </button>
      <button onClick={sendToBackend} className="btn btn-secondary" disabled={!audioBlob}>
        Send to AI
      </button>
    </div>
  );
};

export default App;
