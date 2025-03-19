import { useEffect, useState } from 'react';
import { connectWallet, getCurrentAccount } from '../utils/wallet';

export const useWallet = () => {
    const [account, setAccount] = useState(null);

    const connect = async () => {
        const connectedAccount = await connectWallet();
        setAccount(connectedAccount);
    };

    useEffect(() => {
        const currentAccount = getCurrentAccount();
        if (currentAccount) {
            setAccount(currentAccount);
        }
    }, []);

    return { account, connect };
};
