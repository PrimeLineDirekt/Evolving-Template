'use client';

import { useState } from 'react';
import type { YouTubeVideo } from '@/data/knowledge-content';

interface VideoEmbedProps {
  video: YouTubeVideo;
  autoplay?: boolean;
}

export function VideoEmbed({ video, autoplay = false }: VideoEmbedProps) {
  const [showIframe, setShowIframe] = useState(autoplay);

  const embedUrl = `https://www.youtube.com/embed/${video.id}${autoplay ? '?autoplay=1&mute=1' : ''}`;
  const thumbnailUrl = `https://img.youtube.com/vi/${video.id}/maxresdefault.jpg`;

  if (!showIframe) {
    return (
      <div className="relative group cursor-pointer" onClick={() => setShowIframe(true)}>
        {/* Aspect ratio container */}
        <div className="relative w-full pb-[56.25%] rounded-xl overflow-hidden bg-gray-900">
          {/* Thumbnail */}
          <img
            src={thumbnailUrl}
            alt={video.title}
            className="absolute inset-0 w-full h-full object-cover"
          />

          {/* Play button overlay */}
          <div className="absolute inset-0 flex items-center justify-center bg-black/30 group-hover:bg-black/40 transition-colors">
            <div className="w-20 h-20 rounded-full bg-red-600 group-hover:bg-red-700 group-hover:scale-110 transition-all duration-300 flex items-center justify-center shadow-2xl">
              <svg
                className="w-8 h-8 text-white ml-1"
                fill="currentColor"
                viewBox="0 0 24 24"
              >
                <path d="M8 5v14l11-7z" />
              </svg>
            </div>
          </div>

          {/* Duration badge */}
          <div className="absolute bottom-3 right-3 px-2 py-1 rounded-md bg-black/80 text-white text-xs font-medium">
            {video.duration}
          </div>
        </div>

        {/* Video info */}
        <div className="mt-4">
          <h4 className="text-base font-semibold text-gray-900 mb-1">
            {video.title}
          </h4>
          <p className="text-sm text-gray-600">{video.channel}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="relative">
      {/* Aspect ratio container */}
      <div className="relative w-full pb-[56.25%] rounded-xl overflow-hidden shadow-lg">
        <iframe
          src={embedUrl}
          title={video.title}
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
          className="absolute inset-0 w-full h-full"
          aria-label={`YouTube video: ${video.title}`}
        />
      </div>

      {/* Video info */}
      <div className="mt-4">
        <h4 className="text-base font-semibold text-gray-900 mb-1">
          {video.title}
        </h4>
        <p className="text-sm text-gray-600">{video.channel}</p>
      </div>

      {/* Duration badge */}
      <div className="absolute top-3 right-3 px-2 py-1 rounded-md bg-black/80 text-white text-xs font-medium">
        {video.duration}
      </div>
    </div>
  );
}
