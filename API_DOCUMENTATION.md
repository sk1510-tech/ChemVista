# ChemVista API Documentation

## Overview
ChemVista provides a RESTful API for accessing chemical element and compound data. All endpoints return JSON responses and support CORS for cross-origin requests.

## Base URL
```
Local Development: http://localhost:5000
Production: https://your-domain.com
```

## Authentication
Currently, the API is public and does not require authentication. All endpoints are freely accessible.

## Rate Limiting
- **Development**: No rate limiting
- **Production**: 100 requests per minute per IP address

## Response Format

### Standard Response Structure
```json
{
  "status": "success" | "error",
  "data": {}, 
  "message": "Optional message",
  "meta": {
    "timestamp": "2024-01-01T00:00:00Z",
    "version": "1.0",
    "total": 0
  }
}
```

### HTTP Status Codes
- `200` - Success
- `400` - Bad Request (invalid parameters)
- `404` - Not Found (resource doesn't exist)
- `500` - Internal Server Error

## Endpoints

### Elements API

#### Get All Elements
```http
GET /api/elements
```

**Description**: Retrieve all chemical elements with basic information.

**Response Example**:
```json
{
  "status": "success",
  "data": [
    {
      "atomic_number": 1,
      "symbol": "H",
      "name": "Hydrogen",
      "atomic_mass": 1.008,
      "category": "Reactive nonmetal",
      "group": 1,
      "period": 1
    }
  ],
  "meta": {
    "total": 118,
    "timestamp": "2024-01-01T00:00:00Z"
  }
}
```

#### Get Specific Element
```http
GET /api/elements/{atomic_number}
```

**Parameters**:
- `atomic_number` (integer): Atomic number of the element (1-118)

**Response Example**:
```json
{
  "status": "success",
  "data": {
    "atomic_number": 6,
    "symbol": "C",
    "name": "Carbon",
    "description": "Essential element for all life forms...",
    "atomic_mass": 12.011,
    "block": "p",
    "metallic_character": "Non-metal",
    "physical_state": "Solid",
    "discovery_year": "Ancient",
    "discovered_by": "Ancient civilizations",
    "melting_point": 3550,
    "boiling_point": 4027,
    "ionic_forms": ["C4-", "C4+"],
    "isotopes": ["C-12", "C-13", "C-14"],
    "category": "Reactive nonmetal",
    "group": 14,
    "period": 2,
    "electron_configuration": "[He] 2s2 2p2"
  }
}
```

### Compounds API

#### Get All Compounds
```http
GET /api/compounds
```

**Description**: Retrieve all chemical compounds with basic information.

**Query Parameters**:
- `category` (optional): Filter by compound category
- `limit` (optional): Limit number of results (default: 50)
- `offset` (optional): Offset for pagination (default: 0)

**Response Example**:
```json
{
  "status": "success",
  "data": [
    {
      "id": "water",
      "name": "Water",
      "formula": "H2O",
      "molecular_weight": 18.015,
      "category": "Inorganic compound",
      "state": "Liquid"
    }
  ],
  "meta": {
    "total": 200,
    "returned": 50,
    "offset": 0
  }
}
```

#### Get Specific Compound
```http
GET /api/compounds/{compound_id}
```

**Parameters**:
- `compound_id` (string): Unique identifier for the compound

**Response Example**:
```json
{
  "status": "success",
  "data": {
    "id": "water",
    "name": "Water",
    "formula": "H2O",
    "molecular_weight": 18.015,
    "description": "Essential for all life forms, universal solvent.",
    "melting_point": 0,
    "boiling_point": 100,
    "density": 1.0,
    "state": "Liquid",
    "uses": [
      "Drinking",
      "Cleaning", 
      "Industrial processes",
      "Cooling"
    ],
    "safety": "Generally safe, essential for life",
    "composition": {
      "H": 2,
      "O": 1
    },
    "category": "Inorganic compound"
  }
}
```

### Search API

#### Search Elements and Compounds
```http
GET /api/search
```

**Query Parameters**:
- `q` (required): Search query string
- `type` (optional): Filter by "elements" or "compounds"
- `limit` (optional): Limit number of results (default: 10)

**Description**: Search across elements and compounds by name, symbol, or formula.

**Response Example**:
```json
{
  "status": "success",
  "data": {
    "elements": [
      {
        "atomic_number": 6,
        "symbol": "C",
        "name": "Carbon",
        "match_type": "name"
      }
    ],
    "compounds": [
      {
        "id": "carbon_dioxide",
        "name": "Carbon Dioxide",
        "formula": "CO2",
        "match_type": "formula"
      }
    ]
  },
  "meta": {
    "query": "carbon",
    "total_results": 2,
    "search_time_ms": 15
  }
}
```

#### Search Suggestions (Autocomplete)
```http
GET /api/search/suggestions
```

**Query Parameters**:
- `q` (required): Partial search query
- `limit` (optional): Maximum suggestions (default: 5)

**Response Example**:
```json
{
  "status": "success",
  "data": [
    {
      "text": "Water",
      "type": "compound",
      "formula": "H2O",
      "id": "water"
    },
    {
      "text": "Hydrogen",
      "type": "element",
      "symbol": "H",
      "atomic_number": 1
    }
  ]
}
```

### Statistics API

#### Get System Statistics
```http
GET /api/stats
```

**Description**: Get overview statistics about the database.

**Response Example**:
```json
{
  "status": "success",
  "data": {
    "elements_count": 118,
    "compounds_count": 200,
    "categories": {
      "alkali_metals": 6,
      "noble_gases": 7,
      "halogens": 6,
      "transition_metals": 38
    },
    "compound_categories": {
      "organic": 75,
      "inorganic": 100,
      "pharmaceuticals": 15,
      "minerals": 10
    }
  }
}
```

## Error Responses

### 400 Bad Request
```json
{
  "status": "error",
  "message": "Invalid atomic number. Must be between 1 and 118.",
  "error_code": "INVALID_PARAMETER"
}
```

### 404 Not Found
```json
{
  "status": "error",
  "message": "Element with atomic number 150 not found.",
  "error_code": "RESOURCE_NOT_FOUND"
}
```

### 500 Internal Server Error
```json
{
  "status": "error",
  "message": "An internal server error occurred.",
  "error_code": "INTERNAL_ERROR"
}
```

## SDK and Examples

### JavaScript/Fetch API
```javascript
// Get all elements
fetch('/api/elements')
  .then(response => response.json())
  .then(data => console.log(data));

// Search for compounds
fetch('/api/search?q=water&type=compounds')
  .then(response => response.json())
  .then(data => console.log(data));

// Get specific element
fetch('/api/elements/6')
  .then(response => response.json())
  .then(data => console.log(data));
```

### Python/Requests
```python
import requests

# Base URL
base_url = "http://localhost:5000"

# Get all elements
response = requests.get(f"{base_url}/api/elements")
elements = response.json()

# Search for compounds
response = requests.get(f"{base_url}/api/search", params={
    'q': 'water',
    'type': 'compounds'
})
search_results = response.json()

# Get specific compound
response = requests.get(f"{base_url}/api/compounds/water")
compound = response.json()
```

### cURL Examples
```bash
# Get all elements
curl -X GET "http://localhost:5000/api/elements"

# Search with query
curl -X GET "http://localhost:5000/api/search?q=carbon&limit=5"

# Get specific element
curl -X GET "http://localhost:5000/api/elements/1"

# Get compound details
curl -X GET "http://localhost:5000/api/compounds/water"
```

## Versioning
- Current Version: `v1`
- Version specified in response meta
- Future versions will be available at `/api/v2/`

## CORS Support
The API supports Cross-Origin Resource Sharing (CORS) for browser-based applications:
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: GET, OPTIONS`
- `Access-Control-Allow-Headers: Content-Type`

## Performance Notes
- Average response time: < 50ms
- Data is cached in memory for faster access
- Large datasets are paginated
- Search results are limited to prevent timeouts

## Future API Features
- **Authentication**: User accounts and API keys
- **Rate Limiting**: Enhanced rate limiting with tiers
- **Webhooks**: Real-time data update notifications
- **GraphQL**: Alternative query interface
- **Batch Operations**: Multiple requests in single call
- **Export Formats**: XML, CSV data export options
