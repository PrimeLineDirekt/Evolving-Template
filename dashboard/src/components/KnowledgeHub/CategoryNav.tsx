'use client';

import { aiBasicsCategories, type Category } from '@/data/knowledge-content';

interface CategoryNavProps {
  selectedCategory: string | 'all';
  onChange: (category: string | 'all') => void;
}

export function CategoryNav({ selectedCategory, onChange }: CategoryNavProps) {
  const allOption = {
    id: 'all',
    title: 'Alle',
    icon: '🌍',
    description: 'Alle Kategorien',
    order: 0,
  };

  const categories = [allOption, ...aiBasicsCategories];

  return (
    <nav className="w-full">
      <div className="overflow-x-auto scrollbar-hide">
        <div className="flex gap-2 pb-2 min-w-max">
          {categories.map((category) => {
            const isActive = selectedCategory === category.id;

            return (
              <button
                key={category.id}
                onClick={() => onChange(category.id)}
                className={`
                  px-5 py-3 rounded-xl
                  flex items-center gap-2 whitespace-nowrap
                  transition-all duration-300 ease-out
                  ${
                    isActive
                      ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg scale-105'
                      : 'bg-white text-gray-700 border border-gray-200 hover:border-blue-300 hover:bg-blue-50 hover:shadow-md'
                  }
                `}
                title={category.description}
              >
                <span className="text-lg">{category.icon}</span>
                <span className="font-medium text-sm">{category.title}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Gradient fade at edges for visual hint of scrollability */}
      <style jsx>{`
        .scrollbar-hide {
          -ms-overflow-style: none;
          scrollbar-width: none;
          scroll-behavior: smooth;
        }
        .scrollbar-hide::-webkit-scrollbar {
          display: none;
        }
      `}</style>
    </nav>
  );
}
