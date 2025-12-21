'use client';

import { quickStartItems } from '@/data/knowledge-content';

export function QuickStart() {
  return (
    <section className="mb-12">
      {/* Section Header */}
      <div className="flex items-center gap-3 mb-6">
        <span className="text-3xl">🚀</span>
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Schnellstart</h2>
          <p className="text-gray-500">In 3 Schritten loslegen</p>
        </div>
      </div>

      {/* Quick Start Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {quickStartItems.map((item, index) => (
          <div
            key={item.id}
            className="relative bg-gradient-to-br from-blue-50 to-purple-50 border border-blue-100 rounded-2xl p-6 hover:shadow-lg transition-shadow"
          >
            {/* Step Number */}
            <div className="absolute top-4 right-4 w-8 h-8 flex items-center justify-center rounded-full bg-blue-600 text-white text-sm font-bold">
              {index + 1}
            </div>

            {/* Icon */}
            <div className="text-4xl mb-4">{item.icon}</div>

            {/* Title */}
            <h3 className="text-lg font-semibold text-gray-900 mb-1">
              {item.title}
            </h3>

            {/* Description */}
            <p className="text-sm text-gray-600 mb-4">
              {item.description}
            </p>

            {/* Action */}
            <div className="text-sm text-blue-600 font-medium bg-white rounded-lg p-3 border border-blue-100">
              {item.action}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
