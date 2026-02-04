/**
 * Chat API Service
 * Handles communication with the backend chat API
 */
import { apiClient } from './api-client';

export interface ChatMessage {
  message: string;
  conversation_id?: string;
}

export interface ToolCall {
  tool_name: string;
  parameters: Record<string, any>;
  result: any;
}

export interface ReasoningTrace {
  intent: string;
  confidence: number;
  tool_selected: string | null;
  response_time_ms: number;
}

export interface ChatResponse {
  conversation_id: string;
  response: string;
  tool_calls: ToolCall[];
  reasoning_trace?: ReasoningTrace;
}

/**
 * Send a message to the chat API
 * @param userId - Unique identifier for the user
 * @param message - The chat message object containing message text and optional conversation_id
 * @returns Promise resolving to the chat response
 */
export const sendMessage = async (
  userId: string,
  message: ChatMessage
): Promise<ChatResponse> => {
  try {
    // Use apiClient which automatically includes auth token
    const response = await apiClient.post<ChatResponse>(
      `/${userId}/chat`,
      message
    );
    return response;
  } catch (error: any) {
    // Handle API errors
    const errorMessage = error?.message || 'Failed to send message';
    throw new Error(errorMessage);
  }
};

/**
 * Check if the API is healthy
 * @returns Promise resolving to true if healthy, false otherwise
 */
export const checkHealth = async (): Promise<boolean> => {
  try {
    // Use fetch for health check (no auth needed)
    const baseUrl = process.env.NEXT_PUBLIC_API_URL?.replace('/api', '') || 'http://localhost:8000';
    const response = await fetch(`${baseUrl}/health`, {
      method: 'GET',
    });
    const data = await response.json();
    return data.status === 'healthy';
  } catch (error) {
    return false;
  }
};
