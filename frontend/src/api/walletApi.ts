
import { apiClient } from './client';
import type {
    MockTopUpRequest,
    TeacherEarnings,
    WalletBalance,
    WalletTransaction,
    } from '../types/payment';

export async function getWalletBalance(): Promise<WalletBalance> {

    const response = await apiClient.get<WalletBalance>('/wallet/me');

    return response.data;

    }

export async function getWalletTransactions(): Promise<WalletTransaction[]> {

    const response = await apiClient.get<WalletTransaction[]>('/wallet/me/transactions');

    return response.data;


    }

export async function createMockTopUp(
    data: MockTopUpRequest,
    ): Promise<WalletTransaction> {

        const response = await apiClient.post<WalletTransaction>('/wallet/mock-top-ups', data);

        return response.data;

        }

export async function getTeacherEarnings(): Promise<TeacherEarnings> {

    const response = await apiClient.get<TeacherEarnings>('/wallet/me/earnings');

    return response.data;
    }


