# Sacbeh - Technical and Non-Technical Specifications

## Project Overview

**Sacbeh** is a data visualization application based on the concept that corporate data can be seen as a network of paths that can be traversed. The name "Sacbeh" comes from the Mayan word for "white path."

## Core Concept

### Philosophy
- Data visualization as a network of traversable paths
- Corporate data exploration through path traversal
- Users "follow white paths" through their data landscape

### User Journey
1. Load dataset → View as aggregated path
2. Click to traverse deeper into data
3. Switch dimensions for "path detours"
4. Continue exploration through the data network

## Visual Design System

### Color Palette
- **Mayan Blue** (#0066cc) - Primary accents
- **Orange** - Action accents
- **White** - Neutral accents
- **Dark Grey** (#2d2d2d) - Background

### Design Principles
- Modern minimalist dark mode aesthetic
- Subtle geometric patterns in background
- Clean, uncluttered interface
- Focus on data visualization

## Technical Architecture

### Frontend Layer
- **Framework**: Streamlit
- **Visualization**: Vega-Altair (Vega-Lite compliant)
- **UI Style**: Dark mode with Mayan blue, orange, and white accents

### Controller Layer (Singleton)
- **Pattern**: Python Singleton
- **Purpose**: Shared across frontend and future API server
- **Responsibilities**: 
  - State management
  - Data processing coordination
  - Path traversal logic

### Model Layer
- **Purpose**: Path definition and configuration (not data modeling)
- **Standard**: Vega-Lite compliance
- **Focus**: Path metadata and structure modeling

### AI Agent Layer
- **Purpose**: Intelligent data source analysis and path discovery
- **Capabilities**:
  - Analyze data source structure
  - Identify corporate process data (sales, production, inventory, etc.)
  - Generate SQL queries for data retrieval
  - Identify dimension fields automatically
  - Generate Vega-Lite path declarations
  - Understand data nature and structure

### Data Processing Layer
- **Pattern**: Abstract Factory for DataFrame handlers
- **Current**: Pandas implementation
- **Future**: PySpark implementation (interchangeable)
- **Requirement**: Same interface for seamless switching

### Database Layer
- **Pattern**: Abstract Factory for database connectors
- **Purpose**: Seamless switching between data sources
- **Requirement**: Unified interface regardless of underlying database

## Design Patterns

1. **Singleton Controller** - Shared state management
2. **Abstract Factory (Database)** - Data source abstraction
3. **Abstract Factory (DataFrame)** - Processing engine abstraction
4. **Vega-Lite Standard** - Path definition protocol
5. **MVC Separation** - Clear component boundaries

## Core Functionality

### Data Loading
- Connect to relational databases
- Support for multiple data source types
- Large dataset handling capabilities
- AI-powered data source analysis

### Path Identification
- Datasets become "paths"
- AI-powered automatic dimension discovery
- Intelligent corporate process identification
- Path metadata management

### Dimension Aggregation
- Fields become "dimensions" for data grouping
- Default dimension selection
- Dynamic dimension switching

### Data Visualization
- Dynamic charts based on dimension aggregation
- Vega-Lite compliant visualizations
- Interactive chart elements

### Path Traversal
- Click to zoom into chart dimension items
- Navigate deeper into data hierarchy
- Maintain context during traversal

### Path Detours
- Switch aggregation dimensions at current path level
- Apply new dimensions to current data view
- Seamless dimension switching

## Technical Stack

### Core Dependencies
- `streamlit==1.28.1` - Main UI framework
- `pydantic==2.5.0` - Data validation and modeling
- `python-dotenv==1.0.0` - Environment configuration
- `email-validator==2.2.0` - Email validation

### Data Visualization
- `altair==5.5.0` - Vega-Lite compliant visualizations
- `plotly==6.2.0` - Additional interactive charts

### Data Processing
- `pandas==2.3.1` - Initial DataFrame handler
- `numpy==1.26.4` - Numerical computing support
- `setuptools==80.9.0` - Package management

### Database Connectivity
- `sqlalchemy==2.0.41` - Database abstraction layer
- `psycopg2-binary==2.9.10` - PostgreSQL adapter

## Future Extensibility

### API Server
- FastAPI or Flask integration
- Same controller instantiation
- RESTful API endpoints

### Additional Data Sources
- **Relational**: MySQL, SQL Server, Oracle
- **NoSQL**: MongoDB, Cassandra, Redis
- **Cloud**: BigQuery, Redshift, Snowflake
- **APIs**: REST, GraphQL, gRPC
- **Files**: CSV, JSON, Parquet, Excel

### Processing Engines
- PySpark integration
- Dask for distributed computing
- GPU acceleration support

### AI/ML Capabilities
- Natural language processing for data understanding
- Schema analysis and pattern recognition
- Query generation and optimization
- Corporate process classification

### Visualization Enhancements
- 3D data visualization
- Network graph representations
- Real-time data streaming

## Data Flow Architecture

```
Data Sources → AI Agent (Analysis) → Abstract Factory (DB) → DataFrame Handler (Pandas/PySpark) 
    ↓
Controller (Singleton) → Vega-Lite Paths → Vega-Altair Visualization → Streamlit UI
```

## Development Guidelines

### Code Organization
- MVC architecture with clear separation
- Abstract factory patterns for extensibility
- Type hints and comprehensive documentation
- Unit and integration testing support

### Performance Considerations
- Large dataset handling
- Efficient data streaming
- Memory optimization
- Caching strategies

### Security
- Data validation with Pydantic
- Secure database connections
- Input sanitization
- Access control mechanisms

## Current Status

### Completed
- ✅ Project structure and MVC setup
- ✅ Virtual environment configuration
- ✅ Dependencies installation
- ✅ Welcome page with minimalist design
- ✅ Basic controller singleton implementation
- ✅ Pydantic models for data structures

### In Progress
- 🔄 Database connector abstract factory
- 🔄 DataFrame handler abstract factory
- 🔄 Vega-Lite path models
- 🔄 Data visualization components

### Planned
- 📋 AI agent implementation
- 📋 Path traversal logic
- 📋 Dimension switching functionality
- 📋 Interactive chart components
- 📋 Data source integration
- 📋 API server implementation

---

*This document will be updated as new specifications are provided and implementation progresses.* 