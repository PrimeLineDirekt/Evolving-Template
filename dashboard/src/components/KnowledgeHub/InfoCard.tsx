'use client';

import { useState } from 'react';
import type { InfoCard as InfoCardType } from '@/data/knowledge-content';

interface InfoCardProps {
  card: InfoCardType;
  onOpenDetail: (card: InfoCardType) => void;
  isRead?: boolean; // Track if user has read this card
}

// Skill level badge configuration
const skillLevelConfig = {
  beginner: { emoji: '🌱', label: 'Anfänger', color: 'bg-green-100 text-green-700 border-green-200' },
  advanced: { emoji: '🌿', label: 'Fortgeschritten', color: 'bg-orange-100 text-orange-700 border-orange-200' },
  expert: { emoji: '🌳', label: 'Experte', color: 'bg-purple-100 text-purple-700 border-purple-200' }
};

export function InfoCard({ card, onOpenDetail, isRead = false }: InfoCardProps) {
  const [isHovered, setIsHovered] = useState(false);

  const skillConfig = skillLevelConfig[card.skillLevel];
  const hasVideos = card.fullContent.videos && card.fullContent.videos.length > 0;

  return (
    <button
      onClick={() => onOpenDetail(card)}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      className={`
        relative w-full text-left p-6 rounded-2xl
        bg-white border border-gray-200
        shadow-sm hover:shadow-lg
        transition-all duration-300 ease-out
        ${isHovered ? 'scale-[1.02] -translate-y-1' : ''}
        group cursor-pointer
      `}
    >
      {/* Skill Level Badge - Top Right */}
      <div className="absolute top-3 right-3 flex items-center gap-2">
        <div className={`
          flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium border
          ${skillConfig.color}
        `}>
          <span>{skillConfig.emoji}</span>
          <span className="hidden sm:inline">{skillConfig.label}</span>
        </div>
      </div>

      {/* Read Checkmark - Top Left */}
      {isRead && (
        <div className="absolute top-3 left-3">
          <div className="w-6 h-6 flex items-center justify-center rounded-full bg-green-100 border border-green-200">
            <svg className="w-4 h-4 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
        </div>
      )}

      {/* Icon */}
      <div className="text-4xl mb-4 mt-2">{card.icon}</div>

      {/* Title */}
      <h3 className="text-lg font-semibold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors pr-24">
        {card.title}
      </h3>

      {/* Category Tag */}
      <div className="mb-2">
        <span className="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium bg-gray-100 text-gray-600">
          {card.category}
        </span>
      </div>

      {/* Short Description */}
      <p className="text-sm text-gray-600 leading-relaxed mb-3">
        {card.shortDescription}
      </p>

      {/* Metadata Row */}
      <div className="flex items-center gap-3 text-xs text-gray-500 mb-3">
        {/* Estimated Read Time */}
        <div className="flex items-center gap-1">
          <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>~{card.estimatedReadTime} min</span>
        </div>

        {/* Video Indicator */}
        {hasVideos && (
          <div className="flex items-center gap-1 text-purple-600">
            <span>🎬</span>
            <span>{card.fullContent.videos!.length} Video{card.fullContent.videos!.length > 1 ? 's' : ''}</span>
          </div>
        )}
      </div>

      {/* "Mehr erfahren" indicator */}
      <div className={`
        mt-4 flex items-center gap-1 text-sm font-medium text-blue-600
        transition-all duration-300
        ${isHovered ? 'translate-x-1' : ''}
      `}>
        <span>Mehr erfahren</span>
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
        </svg>
      </div>

      {/* Subtle gradient overlay on hover */}
      <div className={`
        absolute inset-0 rounded-2xl pointer-events-none
        bg-gradient-to-br from-blue-50/50 to-purple-50/50
        transition-opacity duration-300
        ${isHovered ? 'opacity-100' : 'opacity-0'}
      `} />
    </button>
  );
}
