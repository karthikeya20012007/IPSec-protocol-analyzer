import { Link, useLocation } from 'react-router-dom';
import { useAppContext } from '../../context/AppContext';
import { SeverityBadge } from '../common/SeverityBadge';
import { 
    DocumentTextIcon, 
    Squares2X2Icon, 
    ArrowsRightLeftIcon, 
    LockClosedIcon, 
    ShieldCheckIcon, 
    DocumentChartBarIcon 
} from '@heroicons/react/24/outline';

const navItems = [
    { path: '/app', label: 'Captures', icon: DocumentTextIcon },
    { path: '/app/overview', label: 'Overview', icon: Squares2X2Icon },
    { path: '/app/traffic', label: 'Traffic', icon: ArrowsRightLeftIcon },
    { path: '/app/ipsec', label: 'IPsec', icon: LockClosedIcon },
    { path: '/app/security', label: 'Security', icon: ShieldCheckIcon },
    { path: '/app/reports', label: 'Reports', icon: DocumentChartBarIcon },
];

export const Shell: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const { currentScenario } = useAppContext();
    const location = useLocation();

    return (
        <div className="min-h-screen bg-[#080909] text-[#8B9299] flex selection:bg-white/10 selection:text-white font-sans">
            {/* Sidebar */}
            <aside className="print:hidden w-64 bg-[#0D0F10] border-r border-[#202326] flex flex-col shrink-0 relative z-20">
                <div className="h-16 flex items-center px-6 border-b border-[#202326] bg-[#0D0F10]/50 backdrop-blur">
                    <Link to="/" className="text-[#E5E7EB] font-medium text-sm tracking-widest uppercase flex items-center space-x-3">
                        <div className="w-5 h-5 bg-white/10 border border-white/20 flex items-center justify-center rounded-sm">
                            <div className="w-1.5 h-1.5 bg-[#3b82f6] rounded-sm"></div>
                        </div>
                        <span>IPsec Analyzer</span>
                    </Link>
                </div>
                <nav className="flex-1 py-6">
                    <div className="text-xs uppercase tracking-widest text-[#636C73] mb-4 px-6 font-medium">ANALYSIS</div>
                    <ul className="space-y-1">
                        {navItems.map(item => {
                            const active = location.pathname === item.path;
                            const IconComponent = item.icon;
                            return (
                                <li key={item.path} className="px-3">
                                    <Link
                                        to={item.path}
                                        className={`flex items-center h-10 px-3 transition-colors rounded-sm ${
                                            active
                                                ? 'bg-[#101213] text-[#E5E7EB] shadow-[inset_3px_0_0_0_#3b82f6]'
                                                : 'text-[#8B9299] hover:bg-white/5 hover:text-[#E5E7EB]'
                                        }`}
                                    >
                                        <IconComponent 
                                            className={`w-4 h-4 shrink-0 ${active ? 'text-[#3b82f6]' : 'text-[#636C73]'}`} 
                                        />
                                        <span className={`ml-2.5 text-sm ${active ? 'font-medium' : ''}`}>{item.label}</span>
                                    </Link>
                                </li>
                            );
                        })}
                    </ul>
                </nav>
            </aside>

            {/* Main Content */}
            <div className="flex-1 flex flex-col min-w-0 relative">
                {/* Context Header */}
                <header className="print:hidden h-16 bg-[#0D0F10] border-b border-[#202326] px-8 flex items-center justify-between shrink-0 sticky top-0 z-10 backdrop-blur-md bg-opacity-95">
                    {currentScenario ? (
                        <div className="flex items-center h-full space-x-6 overflow-x-auto custom-scrollbar">
                            <div className="flex items-center space-x-3">
                                <span className="text-xs text-[#636C73] uppercase tracking-widest font-medium">CAPTURE</span>
                                <span className="text-[#E5E7EB] font-mono text-[13px] bg-[#080909] px-2.5 py-1 rounded-sm border border-[#202326] whitespace-nowrap">
                                    {currentScenario.capture.filename}
                                </span>
                            </div>
                            <div className="w-px h-5 bg-[#202326]"></div>
                            <div className="flex items-center space-x-3">
                                <span className="text-xs text-[#636C73] uppercase tracking-widest font-medium">RISK</span>
                                <SeverityBadge severity={currentScenario.risk_level} />
                                <span className="text-[#E5E7EB] font-mono text-[13px]">{currentScenario.security_score}/100</span>
                            </div>
                            <div className="w-px h-5 bg-[#202326]"></div>
                            <div className="flex items-center space-x-2.5 font-mono text-[13px] whitespace-nowrap">
                                <span className="text-[#3b82f6]">{currentScenario.ipsec.ike_version}</span>
                                <span className="text-[#202326]">/</span>
                                <span className="text-[#E5E7EB]">{currentScenario.ipsec.encryption}</span>
                                <span className="text-[#202326]">/</span>
                                <span className="text-[#E5E7EB]">{currentScenario.ipsec.integrity}</span>
                                <span className="text-[#202326]">/</span>
                                <span className="text-[#8B9299]">{currentScenario.ipsec.ipv6 ? 'IPv6' : 'IPv4'}</span>
                                <span className="text-[#202326]">/</span>
                                <span className="text-[#8B9299]">{currentScenario.ipsec.protocol}</span>
                            </div>
                        </div>
                    ) : (
                        <div className="flex items-center space-x-3 text-sm">
                            <div className="w-2 h-2 rounded-full bg-amber-500/50 animate-pulse"></div>
                            <span className="text-[#636C73] text-xs uppercase tracking-widest font-medium">AWAITING CAPTURE CONTEXT</span>
                        </div>
                    )}
                </header>

                {/* Page Content */}
                <main className="flex-1 p-8 overflow-auto">
                    <div className="max-w-[1600px] mx-auto">
                        {children}
                    </div>
                </main>
            </div>
        </div>
    );
};
