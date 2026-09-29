import React from 'react';
import { Link } from 'react-router-dom';

export const LandingPage: React.FC = () => {
    return (
        <div className="relative min-h-screen bg-[#050505] overflow-hidden flex flex-col font-sans selection:bg-slate-700 selection:text-white">
            
            {/* --- CINEMATIC VIDEO BACKGROUND --- */}
            <div className="absolute inset-0 z-0 overflow-hidden pointer-events-none bg-[#050505]">
                {/* 
                    The video provides the V-shaped light streams, volumetric clouds, 
                    forward motion, and central convergence. 
                */}
                <video 
                    autoPlay 
                    loop 
                    muted 
                    playsInline 
                    className="absolute inset-0 w-full h-full object-cover animate-camera-push opacity-90 mix-blend-screen"
                    poster="/poster.jpg"
                    style={{ filter: 'saturate(0.6) contrast(1.1)' }}
                >
                    <source src="/background.mp4" type="video/mp4" />
                </video>

                {/* 
                    Cinematic Photographic Overlay
                    A subtle gradient that darkens the composition to natural charcoal/midnight, 
                    toning down artificial cyan and giving the footage a premium film look. 
                */}
                <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,rgba(5,5,5,0.4)_20%,rgba(5,5,5,0.85)_80%)]"></div>
                <div className="absolute inset-0 bg-gradient-to-b from-[#050505]/80 via-transparent to-[#050505]/95"></div>
            </div>

            {/* --- HEADER --- */}
            <header className="relative z-20 w-full flex items-center justify-between px-6 md:px-12 py-8 animate-fade-in-down" style={{ animationDelay: '100ms', animationFillMode: 'both' }}>
                <div className="flex items-center space-x-3 cursor-default">
                    <div className="w-5 h-5 bg-white/10 border border-white/20 flex items-center justify-center">
                        <div className="w-1.5 h-1.5 bg-white"></div>
                    </div>
                    <span className="text-white font-semibold tracking-wide text-sm">IPsec Analyzer</span>
                </div>
                <nav className="hidden md:flex items-center space-x-10 text-sm font-medium text-slate-300">
                    <a href="#" className="hover:text-white transition-colors duration-300">Product</a>
                    <a href="#" className="hover:text-white transition-colors duration-300">Architecture</a>
                    <Link to="/app" className="text-white hover:text-slate-300 transition-colors duration-300">Try Application</Link>
                </nav>
            </header>


            {/* --- HERO CONTENT --- */}
            <main className="relative z-20 flex-1 flex flex-col items-center justify-center px-4 sm:px-6 md:px-12 text-center mt-[-40px]">
                
                {/* Technical Label */}
                <div className="flex items-center space-x-2 mb-6 text-slate-400 text-xs font-medium tracking-[0.15em] uppercase animate-fade-in-up" style={{ animationDelay: '300ms', animationFillMode: 'both' }}>
                    <div className="w-1.5 h-1.5 bg-cyan-600/80 rounded-full"></div>
                    <span>AI-Driven IPsec Security Analysis</span>
                </div>
                
                {/* Headline */}
                <h1 className="max-w-4xl text-4xl sm:text-5xl md:text-6xl font-medium text-white tracking-tight leading-[1.15] mb-6 animate-fade-in-up" style={{ animationDelay: '400ms', animationFillMode: 'both' }}>
                    See What Your <br className="hidden sm:block"/> Encrypted Traffic Reveals.
                </h1>
                
                {/* Description */}
                <p className="max-w-xl text-lg text-slate-300 font-normal leading-relaxed mb-10 animate-fade-in-up" style={{ animationDelay: '500ms', animationFillMode: 'both' }}>
                    Analyze IPsec protocol configuration, encrypted traffic behavior, and security posture without decrypting payloads.
                </p>
                
                {/* Primary Restrained CTA */}
                <Link 
                    to="/app"
                    className="group relative inline-flex items-center justify-center px-8 py-3.5 rounded bg-white/5 hover:bg-white/10 border border-white/10 backdrop-blur-md text-white font-medium text-sm tracking-wide transition-all duration-300 animate-fade-in-up"
                    style={{ animationDelay: '600ms', animationFillMode: 'both' }}
                >
                    <span className="relative flex items-center transition-transform duration-300">
                        Try the Application 
                        <span className="ml-2 transform group-hover:translate-x-1 transition-transform duration-300 text-slate-400 group-hover:text-white">&rarr;</span>
                    </span>
                </Link>
            </main>


            {/* --- BOTTOM CAPABILITIES --- */}
            <footer className="relative z-20 w-full px-6 md:px-12 pb-10 pt-6 flex flex-col sm:flex-row justify-center sm:justify-between items-center gap-6 animate-fade-in" style={{ animationDelay: '800ms', animationFillMode: 'both' }}>
                <div className="hidden sm:block flex-1 h-[1px] bg-gradient-to-r from-transparent via-white/10 to-transparent"></div>
                
                <div className="flex flex-wrap justify-center gap-x-8 gap-y-4 sm:gap-14">
                    {['IPsec / IKE', 'ESP Traffic', 'AI Classification', 'Security Assessment'].map((item) => (
                        <div key={item} className="flex items-center space-x-2">
                            <div className="w-[3px] h-[3px] bg-slate-500 rounded-sm"></div>
                            <span className="text-slate-400 font-medium text-xs uppercase tracking-widest">
                                {item}
                            </span>
                        </div>
                    ))}
                </div>

                <div className="hidden sm:block flex-1 h-[1px] bg-gradient-to-r from-transparent via-white/10 to-transparent"></div>
            </footer>
            
        </div>
    );
};
