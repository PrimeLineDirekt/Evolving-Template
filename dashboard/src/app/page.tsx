'use client';

import { useState, useMemo } from 'react';
import {
  sections,
  aiBasicsCategories,
  getCardsByLevel,
  getCardsByLevelAndCategory,
  searchCards,
  type InfoCard,
  type SkillLevel
} from '@/data/knowledge-content';
import {
  SectionGrid,
  QuickStart,
  DetailModal,
  LevelFilter,
  CategoryNav,
  SearchBar,
  ProgressBadge,
  useProgress
} from '@/components/KnowledgeHub';

type TabId = 'quickstart' | 'ai-basics' | 'system-guide';

export default function KnowledgeHub() {
  const [activeTab, setActiveTab] = useState<TabId>('quickstart');
  const [selectedCard, setSelectedCard] = useState<InfoCard | null>(null);

  // Filter states for AI Basics
  const [selectedLevel, setSelectedLevel] = useState<SkillLevel | 'all'>('all');
  const [showLowerLevels, setShowLowerLevels] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<string | 'all'>('all');
  const [searchQuery, setSearchQuery] = useState('');

  // Progress tracking
  const { isRead } = useProgress();

  // Get AI basics section
  const aiBasicsSection = sections.find(s => s.id === 'ai-basics')!;

  // Filtered cards for AI Basics
  const filteredCards = useMemo(() => {
    let cards = aiBasicsSection.cards;

    // Search filter (highest priority)
    if (searchQuery.trim()) {
      cards = searchCards(searchQuery);
    } else {
      // Level filter
      if (selectedLevel !== 'all') {
        if (showLowerLevels) {
          // Include lower levels
          const levelOrder: SkillLevel[] = ['beginner', 'advanced', 'expert'];
          const selectedIndex = levelOrder.indexOf(selectedLevel);
          const includeLevels = levelOrder.slice(0, selectedIndex + 1);
          cards = cards.filter(card => includeLevels.includes(card.skillLevel));
        } else {
          cards = getCardsByLevel(selectedLevel);
        }
      }

      // Category filter
      if (selectedCategory !== 'all') {
        cards = cards.filter(card => card.category === selectedCategory);
      }
    }

    return cards;
  }, [aiBasicsSection.cards, selectedLevel, showLowerLevels, selectedCategory, searchQuery]);

  // Get read cards set
  const readCardsSet = useMemo(() => {
    return new Set(filteredCards.filter(card => isRead(card.id)).map(card => card.id));
  }, [filteredCards, isRead]);

  // Total cards for progress
  const totalAiBasicsCards = aiBasicsSection.cards.length;

  const tabs: { id: TabId; label: string; icon: string }[] = [
    { id: 'quickstart', label: 'Schnellstart', icon: '🚀' },
    { id: 'ai-basics', label: 'KI-Grundlagen', icon: '🎓' },
    { id: 'system-guide', label: 'System-Guide', icon: '📖' },
  ];

  // Reset filters when switching tabs
  const handleTabChange = (tabId: TabId) => {
    setActiveTab(tabId);
    if (tabId !== 'ai-basics') {
      setSearchQuery('');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50">
      {/* Hero Header */}
      <header className="relative overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute inset-0 pattern-bg opacity-50" />

        {/* Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-to-r from-blue-600/10 via-purple-600/10 to-pink-600/10" />

        <div className="relative max-w-6xl mx-auto px-6 py-12">
          {/* Logo & Title */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center gap-3 mb-4">
              <span className="text-5xl">🧠</span>
              <h1 className="text-4xl font-bold">
                <span className="gradient-text">Evolving</span>
              </h1>
            </div>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Dein <strong>Knowledge Hub</strong> - Lerne alles über KI, Prompts,
              Agents und wie du das Evolving System optimal nutzt.
            </p>
          </div>

          {/* Navigation Tabs */}
          <nav className="flex justify-center">
            <div className="inline-flex bg-white rounded-2xl p-1.5 shadow-lg border border-gray-200">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => handleTabChange(tab.id)}
                  className={`
                    flex items-center gap-2 px-6 py-3 rounded-xl font-medium text-sm
                    transition-all duration-200
                    ${activeTab === tab.id
                      ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-md'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                    }
                  `}
                >
                  <span>{tab.icon}</span>
                  <span>{tab.label}</span>
                </button>
              ))}
            </div>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-6 py-8">
        {/* Quick Start Tab */}
        {activeTab === 'quickstart' && (
          <div className="animate-fadeIn">
            <QuickStart />

            {/* Additional Info */}
            <div className="mt-12 bg-white rounded-2xl p-8 border border-gray-200 shadow-sm">
              <h3 className="text-xl font-bold text-gray-900 mb-4">
                Was ist Evolving?
              </h3>
              <p className="text-gray-600 leading-relaxed mb-6">
                Evolving ist dein <strong>zweites Gehirn</strong> - ein KI-gestütztes Personal Knowledge System.
                Es erfasst deine Ideen, speichert dein Wissen und findet automatisch Verbindungen,
                die du sonst übersehen würdest.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="flex items-start gap-3 p-4 bg-blue-50 rounded-xl">
                  <span className="text-2xl">💡</span>
                  <div>
                    <div className="font-medium text-gray-900">Ideen erfassen</div>
                    <div className="text-sm text-gray-600">Automatische Analyse & Bewertung</div>
                  </div>
                </div>
                <div className="flex items-start gap-3 p-4 bg-purple-50 rounded-xl">
                  <span className="text-2xl">📚</span>
                  <div>
                    <div className="font-medium text-gray-900">Wissen speichern</div>
                    <div className="text-sm text-gray-600">Semantisch durchsuchbar</div>
                  </div>
                </div>
                <div className="flex items-start gap-3 p-4 bg-pink-50 rounded-xl">
                  <span className="text-2xl">🔗</span>
                  <div>
                    <div className="font-medium text-gray-900">Verbindungen finden</div>
                    <div className="text-sm text-gray-600">KI findet Synergien automatisch</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* AI Basics Tab */}
        {activeTab === 'ai-basics' && (
          <div className="animate-fadeIn">
            {/* Section Header with Progress */}
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6">
              <div className="flex items-center gap-3">
                <span className="text-3xl">🎓</span>
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">KI-Grundlagen</h2>
                  <p className="text-gray-500">Fundierter Einstieg in die Welt der künstlichen Intelligenz</p>
                </div>
              </div>
              <ProgressBadge totalCards={totalAiBasicsCards} />
            </div>

            {/* Search Bar */}
            <div className="mb-6">
              <SearchBar
                value={searchQuery}
                onChange={setSearchQuery}
                resultCount={searchQuery ? filteredCards.length : undefined}
                placeholder="Themen durchsuchen..."
              />
            </div>

            {/* Filters (hidden during search) */}
            {!searchQuery && (
              <div className="space-y-4 mb-8">
                {/* Level Filter */}
                <LevelFilter
                  selectedLevel={selectedLevel}
                  onChange={setSelectedLevel}
                  showLowerLevels={showLowerLevels}
                  onShowLowerLevelsChange={setShowLowerLevels}
                />

                {/* Category Navigation */}
                <CategoryNav
                  selectedCategory={selectedCategory}
                  onChange={setSelectedCategory}
                />
              </div>
            )}

            {/* Cards Grid */}
            <SectionGrid
              section={aiBasicsSection}
              cards={filteredCards}
              onOpenDetail={setSelectedCard}
              readCards={readCardsSet}
            />

            {/* Search hint when filtering yields no results */}
            {filteredCards.length === 0 && !searchQuery && (
              <div className="text-center py-8">
                <p className="text-gray-500">
                  Keine Themen für diese Filter-Kombination gefunden.
                </p>
                <button
                  onClick={() => {
                    setSelectedLevel('all');
                    setSelectedCategory('all');
                  }}
                  className="mt-4 px-4 py-2 text-blue-600 hover:text-blue-700 font-medium"
                >
                  Filter zurücksetzen
                </button>
              </div>
            )}
          </div>
        )}

        {/* System Guide Tab */}
        {activeTab === 'system-guide' && (
          <div className="animate-fadeIn">
            <SectionGrid
              section={sections.find(s => s.id === 'system-guide')!}
              onOpenDetail={setSelectedCard}
            />
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-200 bg-white mt-12">
        <div className="max-w-6xl mx-auto px-6 py-8">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2 text-gray-600">
              <span className="text-xl">🧠</span>
              <span className="font-medium">Evolving Knowledge Hub</span>
            </div>
            <div className="flex items-center gap-6 text-sm text-gray-500">
              <span>Lokales System - keine Daten werden gesendet</span>
              <span className="w-2 h-2 rounded-full bg-green-500" title="Lokal" />
            </div>
          </div>
        </div>
      </footer>

      {/* Detail Modal */}
      <DetailModal
        card={selectedCard}
        onClose={() => setSelectedCard(null)}
      />
    </div>
  );
}
