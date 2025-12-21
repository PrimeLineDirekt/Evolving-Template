'use client';

import { InfoCard } from './InfoCard';
import type { Section, InfoCard as InfoCardType } from '@/data/knowledge-content';

interface SectionGridProps {
  section: Section;
  onOpenDetail: (card: InfoCardType) => void;
  cards?: InfoCardType[]; // Optional: override section.cards with filtered cards
  compact?: boolean; // Optional: use denser grid layout
  readCards?: Set<string>; // Optional: Set of read card IDs
}

export function SectionGrid({
  section,
  onOpenDetail,
  cards,
  compact = false,
  readCards = new Set()
}: SectionGridProps) {
  // Use provided cards or fall back to section.cards
  const displayCards = cards ?? section.cards;
  const cardCount = displayCards.length;

  return (
    <section className="mb-12">
      {/* Section Header */}
      <div className="flex items-center gap-3 mb-6">
        <span className="text-3xl">{section.icon}</span>
        <div className="flex-1">
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-bold text-gray-900">{section.title}</h2>
            {/* Card Count Badge */}
            <span className="px-2 py-0.5 text-sm font-medium bg-blue-100 text-blue-700 rounded-full">
              {cardCount} {cardCount === 1 ? 'Thema' : 'Themen'}
            </span>
          </div>
          <p className="text-gray-500">{section.description}</p>
        </div>
      </div>

      {/* Empty State */}
      {cardCount === 0 && (
        <div className="text-center py-12 px-4 bg-gray-50 rounded-2xl border-2 border-dashed border-gray-300">
          <div className="text-6xl mb-4">🔍</div>
          <h3 className="text-lg font-semibold text-gray-700 mb-2">
            Keine Themen gefunden
          </h3>
          <p className="text-gray-500 text-sm">
            Versuche einen anderen Filter oder durchsuche andere Kategorien
          </p>
        </div>
      )}

      {/* Cards Grid */}
      {cardCount > 0 && (
        <div className={`
          grid gap-4
          ${compact
            ? 'grid-cols-1 md:grid-cols-3 lg:grid-cols-4'
            : 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3'
          }
        `}>
          {displayCards.map((card) => (
            <InfoCard
              key={card.id}
              card={card}
              onOpenDetail={onOpenDetail}
              isRead={readCards.has(card.id)}
            />
          ))}
        </div>
      )}
    </section>
  );
}
