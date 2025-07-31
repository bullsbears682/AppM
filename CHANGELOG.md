# Changelog

All notable changes to VoidSight Analytics will be documented in this file.

## [2.1.3] - 2024-12-15

### Fixed
- Fixed projected revenue showing $0 in results display (Issue #127)
- Resolved payback period showing "N/A months" instead of calculated values
- Improved Chart.js loading reliability with better fallback handling

### Changed
- Replaced client-side calculation mock with proper API integration
- Enhanced error handling for failed API responses
- Removed "temporarily unavailable" chart warning

## [2.1.2] - 2024-12-10

### Added
- Monte Carlo simulation improvements for risk analysis
- Industry-specific ROI benchmarks validation
- Enhanced mobile responsiveness for tablet devices

### Fixed
- Memory leak in chart rendering on repeated calculations
- Currency formatting edge cases for international markets

## [2.1.1] - 2024-12-05

### Fixed
- Race condition in scenario analysis generation
- Timeline validation for edge cases
- CSS styling conflicts on Firefox

## [2.1.0] - 2024-11-28

### Added
- Advanced scenario analysis with confidence intervals
- Enterprise dashboard with export capabilities
- Real-time collaboration features (beta)

### Changed
- Upgraded Chart.js to v4.4.0 for better performance
- Redesigned calculation engine for better accuracy
- Improved API response caching

### Deprecated
- Legacy v1 API endpoints (will be removed in v3.0)

## [2.0.5] - 2024-11-20

### Fixed
- Critical security patch for input validation
- Performance improvements for large datasets
- Browser compatibility issues with Safari

## [2.0.4] - 2024-11-15

### Added
- Bulk calculation support for enterprise clients
- Advanced filtering options in reports
- Custom branding options

### Fixed
- Edge case in NPV calculations for negative cash flows
- Timezone handling in report generation

## [2.0.3] - 2024-11-08

### Changed
- Optimized database queries for faster loading
- Enhanced UI/UX based on user feedback
- Better error messages for validation failures

### Fixed
- Chart rendering issues on mobile devices
- Export functionality for large reports

## [2.0.2] - 2024-11-01

### Added
- Integration with popular CRM systems
- Advanced risk assessment algorithms
- Multi-currency support expansion

### Fixed
- Calculator precision issues with large numbers
- Session timeout handling

## [2.0.1] - 2024-10-25

### Fixed
- Critical bug in ROI percentage calculations
- Database connection pool exhaustion
- Memory optimization for concurrent users

## [2.0.0] - 2024-10-15

### Added
- Complete platform redesign with modern UI
- Advanced financial modeling engine
- Real-time analytics and insights
- Enterprise-grade security features
- API rate limiting and monitoring

### Changed
- Migrated from PHP to Python/Flask backend
- New React-based frontend architecture
- Enhanced database schema for better performance

### Removed
- Legacy calculation methods
- Deprecated API v1 endpoints

## [1.8.3] - 2024-09-20

### Fixed
- Last stable release before v2.0 migration
- Critical security updates
- Performance improvements

---

**Note**: Versions prior to 1.8.3 maintained in separate legacy documentation.