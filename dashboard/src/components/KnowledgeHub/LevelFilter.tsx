'use client';

import type { SkillLevel } from '@/data/knowledge-content';

interface LevelFilterProps {
  selectedLevel: SkillLevel | 'all';
  onChange: (level: SkillLevel | 'all') => void;
  showLowerLevels: boolean;
  onShowLowerLevelsChange: (show: boolean) => void;
}

export function LevelFilter({
  selectedLevel,
  onChange,
  showLowerLevels,
  onShowLowerLevelsChange,
}: LevelFilterProps) {
  const levels: Array<{ id: SkillLevel | 'all'; label: string; icon: string }> = [
    { id: 'all', label: 'Alle', icon: '🌍' },
    { id: 'beginner', label: 'Beginner', icon: '🌱' },
    { id: 'advanced', label: 'Advanced', icon: '🌿' },
    { id: 'expert', label: 'Profi', icon: '🌳' },
  ];

  return (
    <div className="space-y-4">
      {/* Level Buttons */}
      <div className="flex flex-wrap gap-3">
        {levels.map((level) => {
          const isActive = selectedLevel === level.id;

          return (
            <button
              key={level.id}
              onClick={() => onChange(level.id)}
              className={`
                px-5 py-3 rounded-xl font-medium
                transition-all duration-300 ease-out
                flex items-center gap-2
                ${
                  isActive
                    ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg scale-105'
                    : 'bg-white text-gray-700 border border-gray-200 hover:border-blue-300 hover:shadow-md hover:scale-102'
                }
              `}
            >
              <span className="text-lg">{level.icon}</span>
              <span>{level.label}</span>
            </button>
          );
        })}
      </div>

      {/* Show Lower Levels Checkbox */}
      {selectedLevel !== 'all' && (
        <div className="flex items-center gap-2 pl-1">
          <input
            type="checkbox"
            id="show-lower-levels"
            checked={showLowerLevels}
            onChange={(e) => onShowLowerLevelsChange(e.target.checked)}
            className="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500 focus:ring-2 cursor-pointer"
          />
          <label
            htmlFor="show-lower-levels"
            className="text-sm text-gray-600 cursor-pointer select-none"
          >
            Auch niedrigere Level anzeigen
          </label>
        </div>
      )}
    </div>
  );
}
