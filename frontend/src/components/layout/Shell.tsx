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
        <div className="min-h-screen bg-[#0B0C0D] text-[#969CA5] flex selection:bg-white/10 selection:text-white font-sans">
            {/* Sidebar */}
            <aside className="print:hidden w-64 bg-[#111315] border-r border-[#25282C] flex flex-col shrink-0 relative z-20">
                <div className="h-16 flex items-center px-6 border-b border-[#25282C] bg-[#111315]/50 backdrop-blur">
                    <Link to="/" className="text-[#E7E9EC] font-medium text-sm tracking-widest uppercase flex items-center space-x-3">
                        <div className="w-5 h-5 bg-white/10 border border-white/20 flex items-center justify-center rounded-sm">
                            <div className="w-1.5 h-1.5 bg-[#3b82f6] rounded-sm"></div>
                        </div>
                        <span>IPsec Analyzer</span>
                    </Link>
                </div>
                <nav className="flex-1 py-6">
                    <div className="text-xs uppercase tracking-widest text-[#666C75] mb-4 px-6 font-medium">ANALYSIS</div>
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
                                                ? 'bg-[#17191C] text-[#E7E9EC] shadow-[inset_3px_0_0_0_#3b82f6]'
                                                : 'text-[#969CA5] hover:bg-white/5 hover:text-[#E7E9EC]'
                                        }`}
                                    >
                                        <IconComponent 
                                            className={`w-4 h-4 shrink-0 ${active ? 'text-[#3b82f6]' : 'text-[#666C75]'}`} 
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
                <header className="print:hidden h-16 bg-[#111315] border-b border-[#25282C] px-8 flex items-center justify-between shrink-0 sticky top-0 z-10 backdrop-blur-md bg-opacity-95">
                    {currentScenario ? (
                        <div className="flex items-center h-full space-x-6 overflow-x-auto custom-scrollbar">
                            <div className="flex items-center space-x-3">
                                <span className="text-xs text-[#666C75] uppercase tracking-widest font-medium">CAPTURE</span>
                                <span className="text-[#E7E9EC] font-mono text-[13px] bg-[#0B0C0D] px-2.5 py-1 rounded-sm border border-[#25282C] whitespace-nowrap">
                                    {currentScenario.capture.filename}
                                </span>
                            </div>
                            <div className="w-px h-5 bg-[#25282C]"></div>
                            <div className="flex items-center space-x-3">
                                <span className="text-xs text-[#666C75] uppercase tracking-widest font-medium">RISK</span>
                                <SeverityBadge severity={currentScenario.risk_level} />
                                <span className="text-[#E7E9EC] font-mono text-[13px]">{currentScenario.security_score}/100</span>
                            </div>
                            <div className="w-px h-5 bg-[#25282C]"></div>
                            <div className="flex items-center space-x-2.5 font-mono text-[13px] whitespace-nowrap">
                                <span className="text-[#3b82f6]">{currentScenario.ipsec.ike_version}</span>
                                <span className="text-[#25282C]">/</span>
                                <span className="text-[#E7E9EC]">{currentScenario.ipsec.encryption}</span>
                                <span className="text-[#25282C]">/</span>
                                <span className="text-[#E7E9EC]">{currentScenario.ipsec.integrity}</span>
                                <span className="text-[#25282C]">/</span>
                                <span className="text-[#969CA5]">{currentScenario.ipsec.ipv6 ? 'IPv6' : 'IPv4'}</span>
                                <span className="text-[#25282C]">/</span>
                                <span className="text-[#969CA5]">{currentScenario.ipsec.protocol}</span>
                            </div>
                        </div>
                    ) : (
                        <div className="flex items-center space-x-3 text-sm">
                            <div className="w-2 h-2 rounded-full bg-amber-500/50 animate-pulse"></div>
                            <span className="text-[#666C75] text-xs uppercase tracking-widest font-medium">AWAITING CAPTURE CONTEXT</span>
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
