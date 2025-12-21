'use client';

import { useEffect, useState } from 'react';

const STORAGE_KEY = 'evolving_kb_progress';

interface ProgressData {
  [cardId: string]: {
    read: boolean;
    timestamp: number;
  };
}

// Custom hook for progress management
export function useProgress() {
  const [progressData, setProgressData] = useState<ProgressData>({});

  // Load progress from localStorage on mount
  useEffect(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        setProgressData(JSON.parse(stored));
      }
    } catch (error) {
      console.error('Failed to load progress data:', error);
    }
  }, []);

  // Save progress to localStorage whenever it changes
  const saveProgress = (data: ProgressData) => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
      setProgressData(data);
    } catch (error) {
      console.error('Failed to save progress data:', error);
    }
  };

  const isRead = (cardId: string): boolean => {
    return progressData[cardId]?.read || false;
  };

  const markAsRead = (cardId: string) => {
    const newData = {
      ...progressData,
      [cardId]: {
        read: true,
        timestamp: Date.now(),
      },
    };
    saveProgress(newData);
  };

  const markAsUnread = (cardId: string) => {
    const newData = { ...progressData };
    if (newData[cardId]) {
      newData[cardId].read = false;
    }
    saveProgress(newData);
  };

  const toggleRead = (cardId: string) => {
    if (isRead(cardId)) {
      markAsUnread(cardId);
    } else {
      markAsRead(cardId);
    }
  };

  const getProgress = (totalCards: number) => {
    const readCount = Object.values(progressData).filter((item) => item.read).length;
    return {
      read: readCount,
      total: totalCards,
    };
  };

  const resetProgress = () => {
    try {
      localStorage.removeItem(STORAGE_KEY);
      setProgressData({});
    } catch (error) {
      console.error('Failed to reset progress:', error);
    }
  };

  return {
    isRead,
    markAsRead,
    markAsUnread,
    toggleRead,
    getProgress,
    resetProgress,
  };
}

// ProgressBadge Component
interface ProgressBadgeProps {
  totalCards: number;
}

export function ProgressBadge({ totalCards }: ProgressBadgeProps) {
  const { getProgress } = useProgress();
  const { read, total } = getProgress(totalCards);
  const percentage = total > 0 ? (read / total) * 100 : 0;

  return (
    <div className="bg-white rounded-2xl shadow-md p-4 border border-gray-100">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-medium text-gray-700">
          Fortschritt
        </span>
        <span className="text-sm font-bold text-gray-900">
          {read} von {total}
        </span>
      </div>

      {/* Progress bar */}
      <div className="relative h-2 bg-gray-100 rounded-full overflow-hidden">
        <div
          className="absolute inset-y-0 left-0 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 transition-all duration-500 ease-out"
          style={{ width: `${percentage}%` }}
        />
      </div>

      <div className="mt-2 text-xs text-gray-500 text-center">
        {percentage.toFixed(0)}% abgeschlossen
      </div>
    </div>
  );
}

// ReadCheckmark Component
interface ReadCheckmarkProps {
  cardId: string;
  size?: 'sm' | 'md';
}

export function ReadCheckmark({ cardId, size = 'md' }: ReadCheckmarkProps) {
  const { isRead, toggleRead } = useProgress();
  const read = isRead(cardId);

  const sizeClasses = {
    sm: 'w-5 h-5',
    md: 'w-6 h-6',
  };

  return (
    <button
      onClick={(e) => {
        e.stopPropagation(); // Prevent parent click handlers
        toggleRead(cardId);
      }}
      className={`
        ${sizeClasses[size]}
        flex items-center justify-center
        rounded-full border-2 transition-all duration-200
        ${read
          ? 'bg-green-500 border-green-500 hover:bg-green-600 hover:border-green-600'
          : 'bg-white border-gray-300 hover:border-gray-400'
        }
      `}
      title={read ? 'Als ungelesen markieren' : 'Als gelesen markieren'}
    >
      {read && (
        <svg
          className="w-3 h-3 text-white"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={3}
            d="M5 13l4 4L19 7"
          />
        </svg>
      )}
    </button>
  );
}
