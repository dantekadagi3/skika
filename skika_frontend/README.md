# Skika Officers Dashboard

A modern, responsive web-based interface for administrators and officers to manage citizen feedback, track projects, and provide transparent governance through the Skika platform.

## Features

- **Authentication & Authorization**: Secure JWT-based login with role-based access control
- **Reports Management**: View, filter, and update citizen reports with bilingual SMS notifications
- **Projects Tracking**: Monitor development initiatives with budget tracking and progress visualization
- **Analytics & Insights**: Real-time dashboards with data visualization using Recharts
- **Sentiment Analysis**: AI-powered sentiment analysis of citizen feedback (positive, neutral, negative)
- **User Administration**: Manage officers, wards, and audit trails
- **Dark/Light Theme**: Governance-inspired color palette with full theme support
- **Bilingual Support**: English and Swahili translations for all labels

## Technology Stack

- **Framework**: Next.js 16 with TypeScript
- **Styling**: Tailwind CSS v4 with custom design tokens
- **State Management**: SWR for data fetching and caching
- **Charts**: Recharts for data visualization
- **UI Components**: Custom shadcn-inspired components
- **API Client**: Custom implementation with JWT token management

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn
- Access to Skika Backend API (running on http://127.0.0.1:8000)

### Installation

1. Clone the repository
2. Install dependencies:
   \`\`\`bash
   npm install
   \`\`\`

3. Set up environment variables:
   \`\`\`bash
   cp .env.example .env.local
   \`\`\`

4. Update `.env.local` with your API endpoint:
   \`\`\`
   NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api
   \`\`\`

5. Start the development server:
   \`\`\`bash
   npm run dev
   \`\`\`

6. Open [http://localhost:3000](http://localhost:3000) in your browser

## Login Credentials

For development/demo purposes:
- **Phone**: +254712345678
- **Password**: demo123

## Project Structure

\`\`\`
├── app/
│   ├── layout.tsx                 # Root layout
│   ├── page.tsx                   # Entry point (redirects to login/dashboard)
│   ├── login/
│   │   └── page.tsx               # Login page
│   └── dashboard/
│       ├── layout.tsx             # Dashboard layout with sidebar
│       ├── page.tsx               # Main dashboard
│       ├── reports/               # Reports management
│       ├── projects/              # Projects tracking
│       ├── feedback/              # Feedback & sentiment analysis
│       ├── analytics/             # Advanced analytics
│       └── admin/                 # Administration panel
├── components/
│   ├── auth/                      # Authentication components
│   ├── dashboard/                 # Dashboard layout components
│   ├── reports/                   # Reports module components
│   ├── feedback/                  # Feedback & sentiment components
│   ├── admin/                     # Admin module components
│   └── ui/                        # Reusable UI components
├── lib/
│   └── api-client.ts              # API client with JWT management
├── providers/
│   ├── auth-provider.tsx          # Authentication context
│   └── theme-provider.tsx         # Theme management
└── globals.css                    # Global styles & design tokens
\`\`\`

## API Integration

The dashboard connects to the Skika Backend REST API with the following endpoints:

- **Authentication**: `POST /dashboard-login/`
- **Reports**: `GET/POST /reports/`, `POST /reports/{id}/update_status/`
- **Projects**: `GET/POST /projects/`
- **Feedback**: `GET/POST /feedback/`
- **Users**: `GET/POST /dashboard-users/`
- **Analytics**: `GET /dashboard-stats/`
- **Audit Logs**: `GET /audit-logs/`
- **Wards**: `GET /wards/`

## Key Features

### Reports Management
- View all citizen reports with filtering by ward, category, and status
- Update report status with automatic SMS notifications (bilingual)
- Real-time status tracking and audit trails

### Projects Dashboard
- Monitor development projects across wards
- Track budget allocation vs. actual spending
- Visual progress indicators
- Project categorization and status management

### Analytics & Insights
- Dashboard overview with key metrics
- Report distribution by status and category
- Monthly trends and citizen engagement metrics
- Resolution rate tracking

### Sentiment Analysis
- Automatic sentiment classification (positive, neutral, negative)
- Visual sentiment distribution
- Insights and recommendations based on feedback trends
- Integration with citizen ratings

### User Administration
- Create and manage officer accounts
- Role-based access control (Admin, Officer, Leader)
- Ward assignment and management
- Complete audit trail of all actions

## Theming

The dashboard uses a governance-inspired color palette:
- **Primary**: Warm blue (#2563eb) - Trust and stability
- **Secondary**: Purple (#7c3aed) - Transparency and integrity
- **Accent Green**: #10b981 - Inclusion and growth
- **Accent Warm**: #f59e0b - Action and engagement

Supports automatic light/dark mode switching with system preference detection.

## Security

- JWT-based authentication with secure token storage
- Role-based access control (RBAC)
- Audit logging for all administrative actions
- HTTPS enforcement in production
- Secure API communication with Bearer token authentication

## Performance

- Server-side rendering for fast initial load
- Client-side caching with SWR
- Optimized bundle size with Next.js
- Lazy loading of dashboard modules
- Image optimization

## Deployment

### Vercel (Recommended)

1. Push code to GitHub
2. Connect repository to Vercel
3. Set environment variables in Vercel dashboard
4. Deploy

### Other Platforms

The dashboard can be deployed to any Node.js hosting provider:

\`\`\`bash
npm run build
npm start
\`\`\`

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

### Code Style

- TypeScript for type safety
- ESLint configuration for consistency
- Tailwind CSS for styling
- Component-based architecture

## Troubleshooting

### Connection Issues
- Ensure backend API is running on http://127.0.0.1:8000
- Check NEXT_PUBLIC_API_BASE_URL in .env.local
- Verify network connectivity

### Authentication Errors
- Clear browser localStorage
- Check credentials
- Verify JWT token validity
- Check browser console for errors

### Styling Issues
- Clear `.next` folder: `rm -rf .next`
- Rebuild: `npm run build`
- Check CSS is properly imported

## Future Enhancements

- Real-time WebSocket updates for instant notifications
- Export reports to PDF/CSV
- Multi-language support beyond English/Swahili
- Advanced filtering and search
- Integration with Africa's Talking for SMS
- Firebase push notifications
- Mobile-responsive improvements
- Advanced permission management

## Support

For issues and support:
- Email: support@skika-platform.org
- Website: www.skika-platform.org

## License

Copyright © 2025 Skika Platform. All rights reserved.
\`\`\`

```json file="" isHidden
