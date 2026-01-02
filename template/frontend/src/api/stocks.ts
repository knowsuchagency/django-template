import { useQuery } from '@tanstack/react-query'
import { apiFetch } from '@/lib/api'

export interface StockData {
  id: number
  symbol: string
  price: number
  volume: number
  date: string
}

// Query keys factory for better organization
export const stockKeys = {
  all: ['stocks'] as const,
  lists: () => [...stockKeys.all, 'list'] as const,
  list: (filters?: { symbol?: string }) => 
    [...stockKeys.lists(), filters] as const,
  symbols: () => [...stockKeys.all, 'symbols'] as const,
}

// API functions
async function fetchStocks(symbol?: string): Promise<StockData[]> {
  return apiFetch<StockData[]>('/api/v1/example/stocks', {
    params: symbol ? { symbol } : undefined,
  })
}

async function fetchStockSymbols(): Promise<string[]> {
  const stocks = await apiFetch<StockData[]>('/api/v1/example/stocks')
  return [...new Set(stocks.map(stock => stock.symbol))].sort()
}

// Custom hooks
export function useStocks(symbol?: string) {
  return useQuery({
    queryKey: stockKeys.list({ symbol }),
    queryFn: () => fetchStocks(symbol),
    // Stock data is considered fresh for 30 seconds (inherited from queryClient)
    // but we can override here if needed
  })
}

export function useStockSymbols() {
  return useQuery({
    queryKey: stockKeys.symbols(),
    queryFn: fetchStockSymbols,
    staleTime: 5 * 60 * 1000, // Symbols change less frequently, so 5 minutes
    gcTime: 10 * 60 * 1000, // Keep in cache for 10 minutes
  })
}