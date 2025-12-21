'use client';

import { useState, useEffect } from 'react';

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  resultCount?: number;
}

export function SearchBar({
  value,
  onChange,
  placeholder = 'Themen durchsuchen...',
  resultCount
}: SearchBarProps) {
  const [isFocused, setIsFocused] = useState(false);
  const [debouncedValue, setDebouncedValue] = useState(value);

  // Debounce for visual feedback
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, 300);

    return () => clearTimeout(timer);
  }, [value]);

  const handleClear = () => {
    onChange('');
  };

  return (
    <div className="relative w-full">
      {/* Search input container */}
      <div
        className={`
          relative flex items-center gap-3
          px-4 py-3 rounded-xl
          bg-white border-2
          transition-all duration-300
          ${isFocused
            ? 'border-blue-500 shadow-lg shadow-blue-100/50 ring-4 ring-blue-50'
            : 'border-gray-200 shadow-sm hover:border-gray-300 hover:shadow-md'
          }
        `}
      >
        {/* Search icon */}
        <svg
          className={`w-5 h-5 transition-colors ${
            isFocused ? 'text-blue-500' : 'text-gray-400'
          }`}
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          />
        </svg>

        {/* Input */}
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          placeholder={placeholder}
          className="flex-1 outline-none text-gray-900 placeholder:text-gray-400 bg-transparent"
          aria-label="Suche"
          aria-describedby={resultCount !== undefined ? 'search-results-count' : undefined}
        />

        {/* Result count badge */}
        {resultCount !== undefined && value && (
          <div
            id="search-results-count"
            className="px-3 py-1 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 text-white text-xs font-medium whitespace-nowrap"
            role="status"
            aria-live="polite"
          >
            {resultCount} {resultCount === 1 ? 'Ergebnis' : 'Ergebnisse'}
          </div>
        )}

        {/* Clear button */}
        {value && (
          <button
            onClick={handleClear}
            className="p-1 rounded-full hover:bg-gray-100 transition-colors group"
            aria-label="Suche löschen"
            type="button"
          >
            <svg
              className="w-5 h-5 text-gray-400 group-hover:text-gray-600"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        )}
      </div>

      {/* Subtle gradient glow on focus */}
      <div
        className={`
          absolute inset-0 rounded-xl
          bg-gradient-to-r from-blue-500/20 to-purple-500/20
          blur-xl -z-10
          transition-opacity duration-300
          ${isFocused ? 'opacity-100' : 'opacity-0'}
        `}
        aria-hidden="true"
      />
    </div>
  );
}
