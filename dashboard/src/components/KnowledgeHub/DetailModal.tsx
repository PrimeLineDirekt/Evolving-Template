'use client';

import { useEffect, useRef, useState } from 'react';
import type { InfoCard } from '@/data/knowledge-content';
import { VideoEmbed } from './VideoEmbed';
import { useProgress } from './ProgressTracker';

interface DetailModalProps {
  card: InfoCard | null;
  onClose: () => void;
}

export function DetailModal({ card, onClose }: DetailModalProps) {
  const modalRef = useRef<HTMLDivElement>(null);
  const { isRead, markAsRead } = useProgress();
  const [isDetailedExpanded, setIsDetailedExpanded] = useState(false);

  // Close on escape key
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [onClose]);

  // Close on click outside
  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) onClose();
  };

  if (!card) return null;

  const cardIsRead = isRead(card.id);

  // Helper function for skill level badge
  const getSkillLevelConfig = (level: string) => {
    switch (level) {
      case 'beginner':
        return { icon: '🌱', label: 'Anfänger', color: 'bg-green-100 text-green-700' };
      case 'advanced':
        return { icon: '🌿', label: 'Fortgeschritten', color: 'bg-blue-100 text-blue-700' };
      case 'expert':
        return { icon: '🌳', label: 'Experte', color: 'bg-purple-100 text-purple-700' };
      default:
        return { icon: '🌱', label: 'Anfänger', color: 'bg-gray-100 text-gray-700' };
    }
  };

  const skillConfig = getSkillLevelConfig(card.skillLevel);

  const handleMarkAsRead = () => {
    markAsRead(card.id);
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm animate-fadeIn"
      onClick={handleBackdropClick}
    >
      <div
        ref={modalRef}
        className="relative w-full max-w-2xl max-h-[85vh] bg-white rounded-3xl shadow-2xl overflow-hidden animate-slideUp"
      >
        {/* Header */}
        <div className="sticky top-0 bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6 pb-8">
          <button
            onClick={onClose}
            className="absolute top-4 right-4 w-10 h-10 flex items-center justify-center rounded-full bg-white/20 hover:bg-white/30 transition-colors"
          >
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>

          <div className="text-5xl mb-3">{card.icon}</div>
          <h2 className="text-2xl font-bold">{card.title}</h2>
          <p className="text-white/80 mt-1">{card.shortDescription}</p>

          {/* Skill Level and Read Time Badges */}
          <div className="flex items-center gap-3 mt-4">
            <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-sm font-medium ${skillConfig.color} bg-white`}>
              <span>{skillConfig.icon}</span>
              <span>{skillConfig.label}</span>
            </span>
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-sm font-medium bg-white/20 text-white">
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>~{card.estimatedReadTime} min</span>
            </span>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[calc(85vh-180px)]">
          {/* Introduction */}
          <div className="mb-6">
            <p className="text-gray-700 leading-relaxed text-lg">
              {card.fullContent.introduction}
            </p>
          </div>

          {/* Key Points */}
          <div className="mb-6">
            <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">
              Wichtige Punkte
            </h3>
            <ul className="space-y-2">
              {card.fullContent.keyPoints.map((point, index) => (
                <li key={index} className="flex items-start gap-3">
                  <span className="flex-shrink-0 w-6 h-6 flex items-center justify-center rounded-full bg-blue-100 text-blue-600 text-sm font-medium">
                    {index + 1}
                  </span>
                  <span className="text-gray-700">{point}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Examples */}
          {card.fullContent.examples && card.fullContent.examples.length > 0 && (
            <div className="mb-6">
              <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">
                Beispiele
              </h3>
              <div className="space-y-3">
                {card.fullContent.examples.map((example, index) => (
                  <div key={index} className="bg-gray-50 rounded-xl p-4 border border-gray-100">
                    <div className="text-sm font-medium text-gray-900 mb-1">
                      {example.title}
                    </div>
                    <div className="text-gray-600 text-sm font-mono bg-white rounded-lg p-3 border border-gray-200">
                      {example.content}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Tips */}
          {card.fullContent.tips && card.fullContent.tips.length > 0 && (
            <div className="mb-6">
              <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">
                Tipps
              </h3>
              <div className="bg-amber-50 rounded-xl p-4 border border-amber-100">
                <ul className="space-y-2">
                  {card.fullContent.tips.map((tip, index) => (
                    <li key={index} className="flex items-start gap-2 text-amber-900">
                      <span className="text-amber-500">💡</span>
                      <span className="text-sm">{tip}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          {/* Related Topics */}
          {card.fullContent.related && card.fullContent.related.length > 0 && (
            <div className="mb-6">
              <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">
                Verwandte Themen
              </h3>
              <div className="flex flex-wrap gap-2">
                {card.fullContent.related.map((relatedId) => (
                  <span
                    key={relatedId}
                    className="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-sm"
                  >
                    {relatedId}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Videos Section */}
          {card.fullContent.videos && card.fullContent.videos.length > 0 && (
            <div className="mb-6">
              <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-4 flex items-center gap-2">
                <span>📹</span>
                <span>Videos</span>
              </h3>
              <div className="space-y-6">
                {card.fullContent.videos.map((video) => (
                  <VideoEmbed key={video.id} video={video} />
                ))}
              </div>
            </div>
          )}

          {/* Detailed Explanation */}
          {card.fullContent.detailedExplanation && (
            <div className="mb-6">
              <button
                onClick={() => setIsDetailedExpanded(!isDetailedExpanded)}
                className="w-full flex items-center justify-between p-4 bg-gray-50 hover:bg-gray-100 rounded-xl transition-colors text-left"
              >
                <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wide">
                  Ausführliche Erklärung
                </h3>
                <svg
                  className={`w-5 h-5 text-gray-500 transition-transform duration-200 ${
                    isDetailedExpanded ? 'rotate-180' : ''
                  }`}
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              {isDetailedExpanded && (
                <div className="mt-3 p-4 bg-white border border-gray-200 rounded-xl">
                  <p className="text-gray-700 whitespace-pre-wrap leading-relaxed">
                    {card.fullContent.detailedExplanation}
                  </p>
                </div>
              )}
            </div>
          )}

          {/* Common Mistakes */}
          {card.fullContent.commonMistakes && card.fullContent.commonMistakes.length > 0 && (
            <div className="mb-6">
              <div className="bg-amber-50 border-2 border-amber-200 rounded-xl p-5">
                <h3 className="text-sm font-semibold text-amber-800 uppercase tracking-wide mb-3 flex items-center gap-2">
                  <span>⚠️</span>
                  <span>Häufige Fehler</span>
                </h3>
                <ul className="space-y-2">
                  {card.fullContent.commonMistakes.map((mistake, index) => (
                    <li key={index} className="flex items-start gap-3">
                      <span className="flex-shrink-0 w-6 h-6 flex items-center justify-center rounded-full bg-amber-200 text-amber-700 text-sm font-medium mt-0.5">
                        {index + 1}
                      </span>
                      <span className="text-amber-900">{mistake}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          {/* Further Reading */}
          {card.fullContent.furtherReading && card.fullContent.furtherReading.length > 0 && (
            <div className="mb-6">
              <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3 flex items-center gap-2">
                <span>📖</span>
                <span>Weiterführende Links</span>
              </h3>
              <div className="space-y-2">
                {card.fullContent.furtherReading.map((link, index) => (
                  <a
                    key={index}
                    href={link.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-2 p-3 bg-gray-50 hover:bg-blue-50 rounded-lg transition-colors group"
                  >
                    <svg
                      className="w-5 h-5 text-gray-400 group-hover:text-blue-600 flex-shrink-0"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                      />
                    </svg>
                    <span className="text-gray-700 group-hover:text-blue-600 font-medium">
                      {link.title}
                    </span>
                  </a>
                ))}
              </div>
            </div>
          )}

          {/* Mark as Read Button */}
          <div className="pt-4 border-t border-gray-200">
            <button
              onClick={handleMarkAsRead}
              disabled={cardIsRead}
              className={`
                w-full py-3 px-6 rounded-xl font-medium transition-all duration-200
                flex items-center justify-center gap-2
                ${
                  cardIsRead
                    ? 'bg-gray-100 text-gray-500 cursor-default'
                    : 'bg-green-600 hover:bg-green-700 text-white shadow-md hover:shadow-lg'
                }
              `}
            >
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <span>{cardIsRead ? 'Bereits gelesen ✓' : 'Als gelesen markieren ✓'}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
